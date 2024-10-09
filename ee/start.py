from io import BytesIO
import edge_tts
import asyncio
import mss
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from cnocr import CnOcr
from PIL import Image

import time
import os
import re
from pycorrector import Corrector
import uuid
import numpy as np


m = Corrector()

CHUNK_SIZE = 20
VOICE = "zh-CN-XiaoxiaoNeural"
CROP_RATIO = 0.7


async def text_to_speech(text, output_file):
    if len(text) >=  20 or len(text) < 2:
        print(f"{screenshot_uuid} 语音合成内容长度错误 {len(text)} skip: {text}")
        return
    text = m.correct(text)['target']
    print(f"{screenshot_uuid} 语音合成内容（修正后）: {text}")
    # Initialize TTS object
    if len(text) > 10:
        rate = "+65%"
    elif len(text) > 7:
        rate = "+50%"
    elif len(text) > 5:
        rate = "+40%"
    else:
        rate = "+30%"
    communicate = edge_tts.Communicate(text, voice=VOICE,rate=rate)
    # Synthesize speech
    await communicate.save(output_file)
    
    print(f"{screenshot_uuid} 语音合成完成，文件保存在 {output_file}")
    
    # 加载音频文件
    audio = AudioSegment.from_mp3(output_file)
    
    # 播放音频
    play(audio)

    # 删除音频文件
    os.remove(output_file)

def play_audio_chunks(chunks: list[bytes], stream: pyaudio.Stream) -> None:
    stream.write(AudioSegment.from_mp3(BytesIO(b''.join(chunks))).raw_data)
    
async def text_to_speech_stream(text, output_file):
    if len(text) >=  20 or len(text) < 2:
        print(f"{screenshot_uuid} 语音合成内容长度错误 {len(text)} skip: {text}")
        return
    text = m.correct(text)['target']
    print(f"{screenshot_uuid} 语音合成内容（修正后）: {text}")
    # Initialize TTS object
    if len(text) > 10:
        rate = "+65%"
    elif len(text) > 7:
        rate = "+50%"
    elif len(text) > 5:
        rate = "+40%"
    else:
        rate = "+30%"
    
    communicator = edge_tts.Communicate(text, voice=VOICE,rate=rate)
    audio_chunks = []

    pyaudio_instance = pyaudio.PyAudio()
    audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    for chunk in communicator.stream_sync():
        if chunk["type"] == "audio" and chunk["data"]:
            audio_chunks.append(chunk["data"])
            if len(audio_chunks) >= CHUNK_SIZE:
                play_audio_chunks(audio_chunks, audio_stream)
                audio_chunks.clear()

    # Play the rest of the audio
    play_audio_chunks(audio_chunks, audio_stream)
    audio_stream.stop_stream()
    audio_stream.close()


if __name__ == "__main__":
    ocr = CnOcr()
    os.makedirs("mp3", exist_ok=True)  # 确保 mp3 目录存在
    last_text = "NONE"
    black_list = ["腾讯", "选集"]

    with mss.mss() as sct:
        monitor = sct.monitors[2 if len(sct.monitors) > 1 else 1]

    while True:
        # 使用 PIL 进行后台截图
        screenshot_uuid = str(uuid.uuid4())

        # 截取指定区域的截图
        # screenshot = ImageGrab.grab()
        # 裁剪图片 
        # screenshot = screenshot.crop((0, 1400, 2800, 1746))

        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        h, w = img.shape[:2]
        screenshot = img[int(h * CROP_RATIO):h, 0:w]
        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.save("screenshot.png")
        result = ocr.ocr(screenshot)
        text = " ".join([item['text'] for item in result if isinstance(item, dict) and 'text' in item])
        print(f"{screenshot_uuid} 图片识别内容: {text}")  # 打印图片识别内容
        output_file = f"mp3/output_{int(time.time())}.mp3"  # 为每个 mp3 文件生成唯一的文件名
        if last_text.strip() == "":
            last_text = "NONE"
        if text is not None and last_text.strip() not in text.strip() and not any(item in text.strip() for item in black_list):
            # text: 之后盘古大陆 开始分裂 and then pangea began to breaku.p...
            # chinese_text: 之后盘古大陆 开始分裂
            # text: 约是美国国土面积的 1.5 倍 the size ofthe United States, is coverediin .e...
            # chinese_text: 约是美国国土面积的 1.5 倍
            # text: 就时间而言 过去就在我们脚下
            # chinese_text: 就时间而言 过去就在我们脚下
            # 如果前面是中文和数字字母组合（可能包含空格），后面是纯英文，则只取前面部分，使用正则表达式
            match = re.search(r'([\u4e00-\u9fa5\d\.\s]+)([a-zA-Z\s]+)', text)
            if match:
                chinese_text = match.group(1)
                english_text = match.group(2)
                text = chinese_text

            try:
                print(f"{screenshot_uuid} 语音合成内容: {text}")
                asyncio.run(text_to_speech_stream(text, output_file))
            except Exception as e:
                print(f"{screenshot_uuid} 语音合成失败: {e}")
            last_text = text
        else:
            # 等待 x 秒后进行下一次截图
            time.sleep(0.05)
