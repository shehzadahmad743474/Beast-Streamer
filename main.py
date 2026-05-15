import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 GLOBAL CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # <--- HAR BAAR CHECK KARNA!
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

user_queue = [] 
cooldowns = {}
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. THE CHAT SNIPER (V4 - HIGH STABILITY) ---
def chat_sniper():
    global user_queue, cooldowns
    log("💀 Sniper Matrix Active...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    channel_url = f"https://www.youtube.com/channel/{c.author.channelId}"
                    
                    now = time.time()
                    if channel_url in cooldowns and (now - cooldowns[channel_url]) < 60:
                        continue 
                    
                    if not any(u[1] == channel_url for u in user_queue):
                        user_queue.append((author_name, channel_url))
                        log(f"⚡ QUEUED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. THE CYBERPUNK OVERLAY INJECTOR ---
def inject_beast_ui(driver, title, timer_sec=30, mode="PROMO"):
    queue_html = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:5]])
    
    ui_script = f"""
    var ui = document.getElementById('beast-matrix-ui');
    if(ui) ui.remove();
    
    var container = document.createElement('div');
    container.id = 'beast-matrix-ui';
    container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:999999; pointer-events:none; font-family:Monospace; border: 20px solid {"#00ffff" if mode=="PROMO" else "#ff00ff"}; box-sizing:border-box; background:rgba(0,0,0,0.05);';
    
    container.innerHTML = `
        <style>
            @keyframes glitch {{ 0%{{text-shadow: 2px 2px red;}} 50%{{text-shadow: -2px -2px blue;}} 100%{{text-shadow: 2px 2px red;}} }}
            .header {{ background: black; border-bottom: 5px solid cyan; padding: 30px; text-align: center; box-shadow: 0 0 20px cyan; }}
            .title {{ font-size: 60px; color: #00ffff; font-weight: bold; animation: glitch 1s infinite; }}
            .timer {{ font-size: 100px; color: #ffff00; margin-top: 10px; }}
            .queue-box {{ position: absolute; bottom: 200px; left: 40px; background: rgba(0,0,0,0.9); padding: 30px; border-left: 15px solid lime; width: 450px; border-radius: 0 20px 20px 0; }}
            .q-title {{ color: lime; font-size: 40px; margin-bottom: 20px; }}
            .q-item {{ color: white; font-size: 35px; margin-bottom: 10px; border-bottom: 1px solid #333; }}
            .footer {{ position: absolute; bottom: 50px; width: 100%; text-align: center; color: white; font-size: 40px; text-shadow: 0 0 10px red; }}
        </style>
        <div class="header">
            <div class="title">{title}</div>
            <div class="timer" id="beast-timer">{timer_sec}s</div>
        </div>
        <div class="queue-box">
            <div class="q-title">NEXT TARGETS:</div>
            {queue_html}
        </div>
        <div class="footer">🚀 SUBSCRIBE & CHAT TO GET FEATURED! 🚀</div>
    `;
    document.body.appendChild(container);

    var timeLeft = {timer_sec};
    var timerInterval = setInterval(function() {{
        timeLeft--;
        var tDisplay = document.getElementById('beast-timer');
        if(tDisplay) tDisplay.innerText = timeLeft + "s";
        if(timeLeft <= 0) clearInterval(timerInterval);
    }}, 1000);
    """
    driver.execute_script(ui_script)

# --- 3. THE MASTER CONTROLLER ---
def browser_controller():
    global user_queue, cooldowns, total_promoted
    log("💀 Matrix Browser Booting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--kiosk')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    DASHBOARD_URL = "data:text/html,<html><body style='background:#000; color:lime; font-family:monospace; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;'> <h1 style='font-size:100px; border:5px solid lime; padding:50px;'>PROMO MATRIX v9.0</h1> <h2 style='font-size:60px; color:cyan;'>STATUS: SCANNING CHAT...</h2> </body></html>"

    while True:
        if len(user_queue) > 0:
            # Step 1: Transition Dashboard
            driver.get(DASHBOARD_URL)
            inject_beast_ui(driver, "PREPARING INJECTION", timer_sec=5, mode="HOME")
            time.sleep(5)
            
            # Step 2: Inject Promotion
            name, url = user_queue.pop(0)
            log(f"🔥 INJECTING: {name}")
            try:
                driver.get(url)
                time.sleep(3)
                inject_beast_ui(driver, f"TARGET: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                cooldowns[url] = time.time()
                time.sleep(30)
            except: pass
        else:
            if driver.current_url != MY_CHANNEL_URL:
                driver.get(MY_CHANNEL_URL)
                inject_beast_ui(driver, "STATION HOST", timer_sec=10, mode="HOME")
            time.sleep(5)

# --- 4. FFmpeg OVERDRIVE ENGINE ---
def stream_engine():
    log("💀 Pumping 8000K Bitrate to Global Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast",
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "16000k", # ULTIMATE QUALITY
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
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
