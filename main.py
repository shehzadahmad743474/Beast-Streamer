import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 ELITE CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # <--- HAR STREAM PAR YE ID CHECK KARO!
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

user_queue = [] 
cooldowns = {}
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. SMART CHAT SNIPER ---
def chat_sniper():
    global user_queue, cooldowns
    log("🚀 Elite Sniper Matrix Online...")
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
                        log(f"⭐ QUEUED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. ELITE UI INJECTOR (v11) ---
def inject_elite_ui(driver, title, timer_sec=30, mode="PROMO"):
    queue_list = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:5]])
    if not queue_list: queue_list = "<div class='q-item'>Type in chat to join...</div>"

    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('elite-hub-ui');
        if(ui) ui.remove();
        
        var container = document.createElement('div');
        container.id = 'elite-hub-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999999; pointer-events:none; font-family:Sans-Serif; border: 20px solid {"#FFD700" if mode=="PROMO" else "#007BFF"}; box-sizing:border-box; background:rgba(0,0,0,0.02);';
        
        var content = `
            <style>
                .top-bar {{ background: linear-gradient(90deg, #000, #111, #000); border-bottom: 4px solid #FFD700; padding: 25px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }}
                .status-title {{ font-size: 55px; color: #FFD700; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }}
                .timer-box {{ font-size: 90px; color: #FFF; margin-top: 10px; font-family: monospace; }}
                .queue-panel {{ position: absolute; bottom: 250px; left: 40px; background: rgba(0,0,0,0.85); padding: 30px; border-radius: 15px; width: 480px; border: 2px solid #FFD700; }}
                .q-head {{ color: #FFD700; font-size: 35px; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold; }}
                .q-item {{ color: #EEE; font-size: 30px; margin-bottom: 8px; font-family: monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
                .footer-ticker {{ position: absolute; bottom: 0; width: 100%; background: #FF0000; color: white; padding: 20px; text-align: center; font-size: 35px; font-weight: bold; animation: pulse 1.5s infinite; }}
                @keyframes pulse {{ 0% {{ opacity: 0.8; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.8; }} }}
            </style>
            <div class="top-bar">
                <div class="status-title">{title}</div>
                <div class="timer-box" id="elite-timer">{timer_sec}s</div>
            </div>
            <div class="queue-panel">
                <div class="q-head">UP NEXT IN LINE:</div>
                {queue_list}
            </div>
            <div class="footer-ticker">⚠️ LIKE THE STREAM & SUBSCRIBE TO STAY IN QUEUE! ⚠️</div>
        `;

        container.innerHTML = window.beastPolicy ? window.beastPolicy.createHTML(content) : content;
        document.body.appendChild(container);

        var timeLeft = {timer_sec};
        var timerInterval = setInterval(function() {{
            timeLeft--;
            var tDisplay = document.getElementById('elite-timer');
            if(tDisplay) tDisplay.innerText = timeLeft + "s";
            if(timeLeft <= 0) clearInterval(timerInterval);
        }}, 1000);
    }})();
    """
    try: driver.execute_script(ui_script)
    except Exception as e: log(f"UI Error: {e}")

# --- 3. THE ELITE CONTROLLER ---
def browser_controller():
    global user_queue, cooldowns, total_promoted
    log("💀 ELITE Hub Browser Starting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--kiosk')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--disable-features=TrustedTypes-for-Elements,TrustedTypes')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    DASHBOARD_URL = "data:text/html,<html><body style='background:#000; color:gold; font-family:monospace; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; height:100vh; margin:0;'> <h1 style='font-size:110px; border:8px solid gold; padding:60px; border-radius:30px;'>CREATOR HUB V11</h1> <h2 style='font-size:60px; color:#FFF; margin-top:40px;'>WAITING FOR NEW CREATORS...</h2> <p style='font-size:40px; color:gray;'>COMMUNITY GROWTH STATION</p> </body></html>"

    while True:
        try:
            if len(user_queue) > 0:
                # 5s Transition
                driver.get(DASHBOARD_URL)
                inject_elite_ui(driver, "PREPARING SPOTLIGHT", timer_sec=5, mode="HOME")
                time.sleep(5)
                
                # 30s Spotlight
                name, url = user_queue.pop(0)
                log(f"🌟 SPOTLIGHT: {name}")
                driver.get(url)
                time.sleep(4) 
                inject_elite_ui(driver, f"SPOTLIGHT: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                cooldowns[url] = time.time()
                time.sleep(30)
            else:
                if driver.current_url != MY_CHANNEL_URL:
                    driver.get(MY_CHANNEL_URL)
                    inject_elite_ui(driver, "STATION HUB", timer_sec=10, mode="HOME")
                time.sleep(5)
        except Exception as e:
            log(f"Loop Glitch: {e}")
            time.sleep(5)

# --- 4. FFmpeg BROADCAST ENGINE ---
def stream_engine():
    log("💀 Broadcasting 8000K 2K Crystal Quality...")
    ffmpeg_cmd = [
        "ffmpeg", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast",
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "16000k", # MAX BITRATE
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
