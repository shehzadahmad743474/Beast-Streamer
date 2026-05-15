import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 PRO STATION CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # <--- HAR BAAR CHECK KARNA
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Stats & Logic
user_queue = [] # List of [Name, URL, ID]
promoted_ids = set() # Strict No-Duplicate
session_start = datetime.now()
total_hits = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. THE CHAT SNIPER (V5 - ANTI-DUPLICATE) ---
def chat_sniper():
    global user_queue
    log("💀 Sniper Matrix v5 Online...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    author_id = c.author.channelId
                    channel_url = f"https://www.youtube.com/channel/{author_id}"
                    
                    # Prevent duplicates in queue and session
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, channel_url, author_id])
                        log(f"✅ QUEUED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. ELITE DYNAMIC UI INJECTOR ---
def inject_ui(driver, title, timer_sec=30, mode="PROMO"):
    queue_html = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:6]])
    if not queue_html: queue_html = "<div class='q-item' style='color:gray'>Waiting for chat...</div>"
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();
        
        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999999; pointer-events:none; font-family:sans-serif; border: 25px solid {"#00E5FF" if mode=="PROMO" else "#FFD700"}; box-sizing:border-box;';
        
        var content = `
            <style>
                .top-plate {{ background: rgba(0,0,0,0.9); border-bottom: 5px solid cyan; padding: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
                .main-title {{ font-size: 50px; color: white; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; }}
                .highlight {{ color: #00E5FF; }}
                .timer-circle {{ font-size: 100px; color: #FFF; margin-top: 10px; font-weight: bold; text-shadow: 0 0 20px rgba(255,255,255,0.5); }}
                .side-panel {{ position: absolute; top: 300px; left: 40px; background: rgba(0,0,0,0.8); padding: 25px; border-radius: 20px; width: 450px; border: 2px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px); }}
                .q-title {{ color: #00E5FF; font-size: 35px; font-weight: bold; border-bottom: 2px solid #333; margin-bottom: 15px; }}
                .q-item {{ color: #EEE; font-size: 28px; margin-bottom: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-family: monospace; }}
                .bottom-bar {{ position: absolute; bottom: 0; width: 100%; background: linear-gradient(transparent, #FF0000); color: white; padding: 40px 0; text-align: center; font-size: 38px; font-weight: bold; }}
            </style>
            <div class="top-plate">
                <div class="main-title">{title}</div>
                <div class="timer-circle" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="side-panel">
                <div class="q-title">WAITING LIST:</div>
                {queue_html}
            </div>
            <div class="bottom-bar">🔥 LIKE THE STREAM TO JUMP THE QUEUE! 🔥</div>
        `;

        container.innerHTML = window.beastPolicy ? window.beastPolicy.createHTML(content) : content;
        document.body.appendChild(container);

        var seconds = {timer_sec};
        var timerInt = setInterval(function() {{
            seconds--;
            var d = document.getElementById('b-timer');
            if(d) d.innerText = seconds + "s";
            if(seconds <= 0) clearInterval(timerInt);
        }}, 1000);
    }})();
    """
    try: driver.execute_script(ui_script)
    except: pass

# --- 3. THE MASTER CONTROLLER ---
def browser_controller():
    global user_queue, promoted_ids, total_hits
    log("💀 ELITE Studio v12 Booting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com') # Removes browser UI
    opts.add_argument('--force-dark-mode')
    opts.add_argument('--disable-features=TrustedTypes-for-Elements')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    while True:
        try:
            # THE DASHBOARD (Station Hub)
            uptime = str(datetime.now() - session_start).split('.')[0]
            DASHBOARD_HTML = f"""data:text/html,<html><body style='background:#000; color:white; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:20px solid #FFD700; box-sizing:border-box;'>
                <h1 style='font-size:80px; color:gold; margin:0;'>BEAST HUB v12</h1>
                <div style='font-size:45px; text-align:center; background:rgba(255,255,255,0.1); padding:40px; border-radius:30px; border:1px solid gold;'>
                    <p style='color:cyan;'>UPTIME: {uptime}</p>
                    <p>TOTAL PROMOTIONS: {total_hits}</p>
                    <p style='color:lime;'>STATUS: READY FOR INJECTION</p>
                </div>
            </body></html>"""

            if len(user_queue) > 0:
                # 1. Dashboard (5s)
                driver.get(DASHBOARD_HTML)
                inject_ui(driver, "SYSTEM RELOADING", timer_sec=5, mode="HOME")
                time.sleep(5)
                
                # 2. Promotion (30s)
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                
                log(f"🚀 SPOTLIGHT: {name}")
                driver.get(url)
                time.sleep(4)
                inject_ui(driver, f"SPOTLIGHT: <span class='highlight'>{name}</span>", timer_sec=30, mode="PROMO")
                
                total_hits += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                
                # Clear from set after 1 min to allow re-entry
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # Idle: Show Host Channel
                if driver.current_url != MY_CHANNEL_URL:
                    driver.get(MY_CHANNEL_URL)
                    inject_ui(driver, "STATION HOST", timer_sec=10, mode="HOME")
                time.sleep(5)
        except Exception as e:
            log(f"Loop Glitch: {e}")
            time.sleep(5)

# --- 4. BROADCAST ENGINE (SILENT LOGS) ---
def stream_engine():
    log("💀 Pumping 8000K 2K Broadcast...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re", # SILENT LOGS
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast",
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "16000k",
        "-pix_fmt", "yuv420p", "-g", "60",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-map", "0:v", "-map", "1:a", "-f", "flv",
        f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]
    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            time.sleep(3)
        except: pass

if __name__ == "__main__":
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
