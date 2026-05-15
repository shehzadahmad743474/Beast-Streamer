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
# 🔴 TERI STREAM KA ASLI 11-LETTER ID (UPDATE KAR LENA NAYE STREAM KE LIYE)
LIVE_VIDEO_ID = "5of2o7kJRvg" 
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

user_queue = []
current_channel_url = MY_CHANNEL

def log(msg):
    # Flush=True zaroori hai GitHub logs ke liye
    print(msg, flush=True)

def chat_sniper():
    global user_queue
    log(f"💀 Chat Sniper Active. Target ID: [{LIVE_VIDEO_ID}]")
    
    if len(LIVE_VIDEO_ID) != 11:
        log("❌ FATAL: VIDEO ID MUST BE EXACTLY 11 CHARACTERS!")
        return

    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            log("✅ Successfully hooked into YouTube Chat Matrix!")
            
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    # Get user's actual channel URL
                    author_channel_id = c.author.channelId
                    channel_url = f"https://www.youtube.com/channel/{author_channel_id}"
                    
                    log(f"💬 COMMAND -> {author_name} wants promotion!")
                    
                    if channel_url not in user_queue and channel_url != current_channel_url:
                        user_queue.append(channel_url)
                        log(f"[+] Added {author_name} to Queue. Size: {len(user_queue)}")
            
            time.sleep(5)
        except Exception as e:
            log(f"[-] Chat Sniper Error (Wrong Video ID?): {e}")
            time.sleep(10)

def browser_controller():
    global current_channel_url, user_queue
    log("💀 Booting Virtual Chrome Browser inside Xvfb...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--kiosk') # Fullscreen for 1080x1920
    options.add_argument('--window-size=1080,1920')
    options.add_argument('--force-dark-mode')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    while True:
        if len(user_queue) > 0:
            current_channel_url = user_queue.pop(0)
            log(f"[*] Navigating screen to: {current_channel_url}")
            try:
                driver.get(current_channel_url)
                time.sleep(5)
                # Scroll down slightly to show channel content
                driver.execute_script("window.scrollBy(0, 300);")
            except:
                pass
            time.sleep(30) # Promote for 30 seconds
        else:
            if driver.current_url != MY_CHANNEL:
                driver.get(MY_CHANNEL)
                log("[*] Queue empty. Displaying Host Channel.")
            time.sleep(5)

def stream_engine():
    log("💀 Master Encoder Online. Capturing Virtual Display & BGM...")
    
    # FFmpeg MAGIC
    # -i :99.0 : Grabs the Xvfb virtual screen we created
    # -i bgm.mp3 : Grabs the unblockable audio we downloaded
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
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
            log("[!] Stream Drop. Restarting Encoder...")
            time.sleep(3)
        except Exception as e:
            log(f"FFmpeg Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    log("=== BEASTGPT FULL VIRTUAL BROWSER C2 ===")
    time.sleep(3) 
    
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    
    time.sleep(10) # Let the browser load before recording
    stream_engine()
