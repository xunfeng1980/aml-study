import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play
from cnocr import CnOcr
from PIL import ImageGrab
import time
import os

async def text_to_speech(text, output_file):
    # Initialize TTS object
    if len(text) > 5:
        communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural",rate="+100%")
    else:
        communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    
    # Synthesize speech
    await communicate.save(output_file)
    
    print(f"语音合成完成，文件保存在 {output_file}")
    
    # 加载音频文件
    audio = AudioSegment.from_mp3(output_file)
    
    # 播放音频
    play(audio)

if __name__ == "__main__":
    ocr = CnOcr()
    os.makedirs("mp3", exist_ok=True)  # 确保 mp3 目录存在
    last_text = None
    black_list = ["腾讯", "选集"]
    while True:
        # 使用 PIL 进行后台截图

        # 截取指定区域的截图
        screenshot = ImageGrab.grab()
        # 裁剪图片 
        screenshot = screenshot.crop((0, 1400, 2800, 1746))
        screenshot.save("screenshot.png")
        
        result = ocr.ocr(screenshot)
        text = " ".join([item['text'] for item in result if isinstance(item, dict) and 'text' in item])
        print(f"图片识别内容: {text}")  # 打印图片识别内容
        output_file = f"mp3/output_{int(time.time())}.mp3"  # 为每个 mp3 文件生成唯一的文件名
        if text is not None and text != last_text and not any(item in text for item in black_list):
            try:
                asyncio.run(text_to_speech(text, output_file))
            except Exception as e:
                print(f"语音合成失败: {e}")
            last_text = text
        # 等待 x 秒后进行下一次截图
        time.sleep(0.33)