import asyncio
import os
import re
import time
import uuid
from io import BytesIO
from queue import Queue
from threading import Thread
from typing import Any

import cv2
import edge_tts
import mss
import numpy as np
import pyaudio
from cnocr import CnOcr
from PIL import Image
from pycorrector import Corrector
from pydub import AudioSegment

CHUNK_SIZE = 20
VOICE = "zh-CN-XiaoxiaoNeural"
MONITOR_NUMBER = 2
CROP_RATIO = 0.7
BLACK_LIST = ["腾讯", "选集"]


def correct_text(text: str) -> str:
    corrector = Corrector()
    return corrector.correct(text)['target']


def get_tts_rate(text_length: int) -> str:
    if text_length > 10:
        return "+65%"
    elif text_length > 7:
        return "+50%"
    elif text_length > 5:
        return "+40%"
    else:
        return "+30%"


async def text_to_speech_stream(text: str, output_file: str) -> None:
    if len(text) >= 20 or len(text) < 2:
        print(f"{uuid.uuid4()} 语音合成内容长度错误 {len(text)} skip: {text}")
        return

    text = correct_text(text)
    print(f"{uuid.uuid4()} 语音合成内容（修正后）: {text}")

    rate = get_tts_rate(len(text))
    communicator = edge_tts.Communicate(text, voice=VOICE, rate=rate)
    audio_chunks = []

    pyaudio_instance = pyaudio.PyAudio()
    audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    for chunk in communicator.stream_sync():
        if chunk["type"] == "audio" and chunk["data"]:
            audio_chunks.append(chunk["data"])
            if len(audio_chunks) >= CHUNK_SIZE:
                play_audio_chunks(audio_chunks, audio_stream)
                audio_chunks.clear()

    play_audio_chunks(audio_chunks, audio_stream)
    audio_stream.stop_stream()
    audio_stream.close()


def play_audio_chunks(chunks: list[bytes], stream: pyaudio.Stream) -> None:
    stream.write(AudioSegment.from_mp3(BytesIO(b''.join(chunks))).raw_data)


def screenshot_producer(queue: Queue[Any]) -> None:
    ocr = CnOcr()
    last_text = "NONE"

    with mss.mss() as sct:
        monitor = sct.monitors[1 if len(sct.monitors) > 1 else 2]

    while True:
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        h, w = img.shape[:2]
        screenshot = img[int(h * CROP_RATIO):h, 0:w]
        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.save("screenshot.png")
        result = ocr.ocr(screenshot)
        text = " ".join([item['text'] for item in result if isinstance(item, dict) and 'text' in item])
        print(f"{uuid.uuid4()} 图片识别内容: {text}")

        if last_text.strip() == "":
            last_text = "NONE"
        if text is not None and last_text.strip() not in text.strip() and not any(
                item in text.strip() for item in BLACK_LIST):
            match = re.search(r'([\u4e00-\u9fa5\d\.\s]+)([a-zA-Z\s]+)', text)
            if match:
                chinese_text = match.group(1)
                text = chinese_text

            queue.put(text)
            last_text = text
        time.sleep(0.1)


def tts_consumer(queue: Queue[Any]) -> None:
    while True:
        text = queue.get()
        if text is None:
            break

        output_file = f"mp3/output_{int(time.time())}.mp3"
        try:
            print(f"{uuid.uuid4()} 语音合成内容: {text}")
            asyncio.run(text_to_speech_stream(text, output_file))
        except Exception as e:
            print(f"{uuid.uuid4()} 语音合成失败: {e}")

        queue.task_done()


def main() -> None:
    os.makedirs("mp3", exist_ok=True)

    queue: Queue[Any] = Queue()

    producer_thread = Thread(target=screenshot_producer, args=(queue,))
    consumer_thread = Thread(target=tts_consumer, args=(queue,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    queue.put(None)
    consumer_thread.join()


if __name__ == "__main__":
    main()
