import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 BROADCAST CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # HAR NAYI STREAM PAR YE ID UPDATE KARNA
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Data Management
user_queue = [] # List of (name, channel_url)
cooldowns = {}  # channel_url -> last_promoted_time
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. CHAT SNIPER (With 1 Min Cooldown Logic) ---
def chat_sniper():
    global user_queue, cooldowns
    log("💀 Chat Sniper Active...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    channel_url = f"https://www.youtube.com/channel/{c.author.channelId}"
                    
                    now = time.time()
                    # Check Cooldown (60 seconds)
                    if channel_url in cooldowns and (now - cooldowns[channel_url]) < 60:
                        continue # Skip if recently promoted
                    
                    # Add to queue if not already there
                    if not any(u[1] == channel_url for u in user_queue):
                        user_queue.append((author_name, channel_url))
                        log(f"➕ Added to Queue: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. JAVASCRIPT OVERLAY INJECTION ---
def inject_overlay(driver, title, mode="promo", timer=30):
    queue_list_html = "".join([f"<li>{u[0]}</li>" for u in user_queue[:5]])
    
    js_code = f"""
    var old = document.getElementById('beast-ui');
    if(old) old.remove();
    var div = document.createElement('div');
    div.id = 'beast-ui';
    div.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:2147483647; pointer-events:none; font-family:Arial; color:white; background:rgba(0,0,0,0.1); border: 15px solid {"#ff0000" if mode=="home" else "#00ff00"}; box-sizing:border-box;';
    div.innerHTML = `
        <div style="background:rgba(0,0,0,0.8); padding:20px; text-align:center; border-bottom:5px solid lime;">
            <h1 style="font-size:50px; margin:0; color:lime;">{title}</h1>
            <h2 id="timer" style="font-size:80px; color:yellow;">{timer}s</h2>
        </div>
        <div style="position:absolute; bottom:150px; left:30px; background:rgba(0,0,0,0.8); padding:20px; border-radius:15px; width:400px; border-left:10px solid cyan;">
            <h3 style="color:cyan; font-size:35px; margin-top:0;">⏳ WAITING LINE:</h3>
            <ul style="font-size:30px; list-style:none; padding:0; line-height:1.5;">{queue_list_html}</ul>
        </div>
        <div style="position:absolute; bottom:50px; width:100%; text-align:center;">
            <h2 style="background:black; display:inline-block; padding:10px 30px; font-size:30px; border:2px solid red;">SUBSCRIBE & TYPE TO JOIN!</h2>
        </div>
    `;
    document.body.appendChild(div);
    
    var count = {timer};
    var itv = setInterval(function() {{
        count--;
        var t = document.getElementById('timer');
        if(t) t.innerText = count + "s";
        if(count <= 0) clearInterval(itv);
    }}, 1000);
    """
    driver.execute_script(js_code)

# --- 3. BROWSER CONTROLLER ---
def browser_controller():
    global user_queue, cooldowns, total_promoted
    log("💀 Booting Virtual Browser...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920')
    options.add_argument('--kiosk')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Dashboard / Home Screen Page
    HOME_HTML = f"data:text/html,<html><body style='background:#050505; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:monospace;'> <h1 style='font-size:80px; color:lime;'>BEAST STATION</h1> <div style='font-size:50px; border:2px solid lime; padding:40px; text-align:center;'> <p>TOTAL PROMOTED: <span id='count'>0</span></p> <p style='color:cyan;'>READY FOR NEXT INJECTION...</p> </div> </body></html>"

    while True:
        if len(user_queue) > 0:
            # Transition: Show Home for 5 seconds
            driver.get(HOME_HTML)
            driver.execute_script(f"document.getElementById('count').innerText = '{total_promoted}';")
            inject_overlay(driver, "STATION DASHBOARD", mode="home", timer=5)
            time.sleep(5)
            
            # Promotion: Pick User
            name, url = user_queue.pop(0)
            log(f"🚀 Promoting: {name}")
            try:
                driver.get(url)
                time.sleep(3) # Wait for page
                inject_overlay(driver, f"PROMOTING: {name}", mode="promo", timer=30)
                total_promoted += 1
                cooldowns[url] = time.time() # Start 1 min cooldown
                time.sleep(30)
            except:
                pass
        else:
            # Stay on Home Screen if queue empty
            if driver.current_url != MY_CHANNEL_URL:
                driver.get(MY_CHANNEL_URL)
                inject_overlay(driver, "HOST CHANNEL", mode="home", timer=10)
            time.sleep(5)

# --- 4. FFmpeg BROADCASTER ---
def stream_engine():
    log("💀 Pumping 2K Bitrate to Shorts Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast",
        "-b:v", "6000k", # High Bitrate for High Quality
        "-maxrate", "6000k", "-bufsize", "12000k",
        "-pix_fmt", "yuv420p", "-g", "60",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-map", "0:v", "-map", "1:a", "-f", "flv",
        f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]
    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            time.sleep(3)
        except:
            time.sleep(3)

if __name__ == "__main__":
    open("current.txt", "w").close() # Fallback files
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(10)
    stream_engine()
