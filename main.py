import os
import subprocess
import threading
import time
import re

# --- 💀 BEASTGPT NAKED CONFIGURATION 💀 ---
# TUNE KAHA THA KUCH HIDE MAT KARNA. TOH YE LE.
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "owsv6D0MvnBNcFLZ"
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"

# Default video jo stream start hone par chalegi (jab tak koi link na bheje)
# Ye NoCopyrightSounds ka ek video hai.
DEFAULT_YT_URL = "https://www.youtube.com/watch?v=jfKfPfyJRdk" 

# Globals
current_media_url = ""
stream_process = None

def get_raw_url(youtube_url):
    import yt_dlp
    print(f"[*] Extracting raw feed from: {youtube_url}")
    ydl_opts = {'format': 'best[ext=mp4]/best', 'quiet': True, 'nocheckcertificate': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

def chat_sniper():
    global current_media_url, stream_process
    import pytchat
    print("💀 Chat Sniper Active. Listening to YouTube Chat...")

    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    msg = c.message
                    # Dhoondo agar kisi ne YouTube link bheja hai
                    urls = re.findall(r'(https?://(?:www\.)?youtu\.?be[^\s]+|https?://(?:www\.)?youtube\.com/watch\?v=[^\s]+)', msg)

                    if urls:
                        target_url = urls[0]
                        print(f"\n🔥 COMMAND RECEIVED FROM CHAT: {c.author.name}")
                        print(f"🔥 Hijacking Stream to: {target_url}")
                        try:
                            # Naya URL extract karo
                            new_url = get_raw_url(target_url)
                            current_media_url = new_url
                            
                            # Purane stream process ko goli maar do
                            if stream_process:
                                print("[!] Killing old stream. Injecting new video...")
                                stream_process.terminate()
                                stream_process.wait()
                        except Exception as e:
                            print(f"[-] Extraction Failed (Video restricted/Live?): {e}")
        except Exception as e:
            print(f"[-] Sniper Error: {e}")
            time.sleep(5)

def stream_engine():
    global stream_process, current_media_url
    print("💀 Beast Encoder Online.")
    
    # Start with default video
    try:
        current_media_url = get_raw_url(DEFAULT_YT_URL)
    except:
        pass # Agar fail hua toh chat aane ka wait karega

    while True:
        if not current_media_url:
            time.sleep(2)
            continue
            
        try:
            # GitHub ka CPU strong hota hai, hum 720p re-encode maarenge 
            # Taki resolutions change hone par YouTube crash na ho.
            ffmpeg_cmd = [
                "ffmpeg",
                "-re",
                "-i", current_media_url,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-b:v", "2500k",
                "-maxrate", "2500k",
                "-bufsize", "5000k",
                "-s", "1280x720", # FORCE 720p HD
                "-g", "60",
                "-c:a", "aac",
                "-b:a", "128k",
                "-ar", "44100",
                "-f", "flv",
                f"{YOUTUBE_RTMP}{STREAM_KEY}"
            ]

            stream_process = subprocess.Popen(ffmpeg_cmd)
            stream_process.wait()
            print("[!] Stream Ended or Interrupted. Auto-Restarting...")
            time.sleep(2)
        except Exception as e:
            print(f"[-] Encoder Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    print("=== BEASTGPT NAKED INTERACTIVE ENGINE ===")
    # Dono kaam ek sath shuru karo (Chat padhna aur Stream karna)
    threading.Thread(target=chat_sniper, daemon=True).start()
    stream_engine()
