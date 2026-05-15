import os
import subprocess
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 NAKED SECRETS 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # ISKO APNE NAYE STREAM SE UPDATE KAR LENA
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL = "https://www.youtube.com/@SHEHZAD_PLAYZ" # Queue khali hone par ye dikhega

user_queue = []
current_channel_url = MY_CHANNEL

def chat_sniper():
    global user_queue
    print(f"💀 Chat Sniper Active. Target ID: [{LIVE_VIDEO_ID}]", flush=True)
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    # Pytchat user ka asli channel ID deta hai
                    author_channel_id = c.author.channelId
                    channel_url = f"https://www.youtube.com/channel/{author_channel_id}"
                    
                    print(f"💬 RECV -> {author_name} wants promotion!", flush=True)
                    
                    if channel_url not in user_queue and channel_url != current_channel_url:
                        user_queue.append(channel_url)
                        print(f"[+] Added {author_name} to Queue.", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"[-] Chat Sniper Error (Wrong Video ID?): {e}", flush=True)
            time.sleep(10)

def browser_controller():
    global current_channel_url, user_queue
    print("💀 Starting Virtual Chrome Browser...", flush=True)
    
    options = webdriver.ChromeOptions()
    # No --headless here because we are running inside Xvfb virtual display
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--kiosk') # Fullscreen force
    options.add_argument('--window-size=1080,1920')
    options.add_argument('--force-dark-mode') # Hacker feel
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    while True:
        if len(user_queue) > 0:
            current_channel_url = user_queue.pop(0)
            print(f"[*] Navigating to: {current_channel_url}", flush=True)
            try:
                driver.get(current_channel_url)
                time.sleep(5)
                # Thoda scroll karega taaki videos dikhein
                driver.execute_script("window.scrollBy(0, 400);")
            except:
                pass
            time.sleep(30) # 30 seconds tak promotion chalega
        else:
            if driver.current_url != MY_CHANNEL:
                driver.get(MY_CHANNEL)
                print("[*] Queue empty. Showing Host Channel.", flush=True)
            time.sleep(5)

def stream_engine():
    print("💀 Master Encoder Online. Capturing Virtual Display...", flush=True)
    
    # FFmpeg MAGIC:
    # -f x11grab : Ye Linux ki virtual screen ko record karta hai
    # -i :99.0 : Ye Display 99 hai jo humne bot.yml mein banayi thi
    # -i bgm.m4a : Ye wo gana hai jo setup ke time download hua
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.m4a",                      
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "2500k",
        "-maxrate", "2500k",
        "-bufsize", "5000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]

    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            print("[!] Stream Drop. Restarting Encoder...", flush=True)
            time.sleep(3)
        except Exception as e:
            print(f"FFmpeg Error: {e}", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    print("=== BEASTGPT FULL VIRTUAL BROWSER C2 ===", flush=True)
    time.sleep(3) # Xvfb display set hone ka wait
    
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    
    # Browser open hone ka wait karo phit recording start karo
    time.sleep(10)
    stream_engine()
