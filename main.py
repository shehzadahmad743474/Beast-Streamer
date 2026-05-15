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

# Data Matrix
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. CHAT SNIPER (V6 - NEURAL SCAN) ---
def chat_sniper():
    global user_queue
    log("💀 Neural Sniper Online...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    author_id = c.author.channelId
                    channel_url = f"https://www.youtube.com/channel/{author_id}"
                    
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, channel_url, author_id])
                        log(f"🧬 QUEUED CREATOR: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. OVERLAY INJECTOR (PUSHES CONTENT DOWN TO SHOW LOGO) ---
def inject_ui(driver, title, timer_sec=30, mode="PROMO"):
    queue_html = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:5]])
    if not queue_html: queue_html = "<div class='q-item' style='color:gray'>Waiting for new voices...</div>"
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        // PUSH YOUTUBE CONTENT DOWN SO LOGO IS VISIBLE
        if ("{mode}" == "PROMO") {{
            document.body.style.paddingTop = "180px";
            var masthead = document.getElementById('masthead-container');
            if(masthead) masthead.style.top = "150px";
        }}

        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();
        
        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:150px; z-index:9999999; pointer-events:none; font-family:sans-serif; background:rgba(0,0,0,0.9); border-bottom: 5px solid {"#00E5FF" if mode=="PROMO" else "#FFD700"}; box-shadow:0 0 20px rgba(0,255,255,0.5);';
        
        var content = `
            <style>
                .top-box {{ display:flex; justify-content:space-between; align-items:center; padding: 20px 40px; height:100%; }}
                .title-txt {{ font-size: 45px; color: white; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; }}
                .t-yellow {{ color: #FFFF00; font-size: 70px; font-weight: bold; font-family: monospace; }}
                .q-panel {{ position: fixed; top: 200px; left: 20px; background: rgba(0,0,0,0.85); padding: 20px; border-radius: 15px; width: 400px; border-left: 8px solid #00E5FF; backdrop-filter: blur(10px); }}
                .q-head {{ color: #00E5FF; font-size: 30px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #333; }}
                .q-item {{ color: #EEE; font-size: 25px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
                .footer-box {{ position: fixed; bottom: 0; width: 100%; background: linear-gradient(90deg, #FF0000, #990000, #FF0000); color: white; padding: 15px; text-align: center; font-size: 32px; font-weight: bold; }}
            </style>
            <div class="top-box">
                <div class="title-txt">{title}</div>
                <div class="t-yellow" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="q-panel">
                <div class="q-head">UP NEXT:</div>
                {queue_html}
            </div>
            <div class="footer-box">🔥 LIKE & SUBSCRIBE TO STAY IN QUEUE! 🔥</div>
        `;

        container.innerHTML = window.beastPolicy ? window.beastPolicy.createHTML(content) : content;
        document.body.appendChild(container);

        var sec = {timer_sec};
        var tInt = setInterval(function() {{
            sec--;
            var d = document.getElementById('b-timer');
            if(d) d.innerText = sec + "s";
            if(sec <= 0) clearInterval(tInt);
        }}, 1000);
    }})();
    """
    try: driver.execute_script(ui_script)
    except: pass

# --- 3. THE MASTER CONTROLLER ---
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Neural Browser Hub Booting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com') 
    opts.add_argument('--force-dark-mode')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    while True:
        try:
            # --- 📡 THE HUB DASHBOARD (Visual Masterpiece) ---
            uptime = str(datetime.now() - session_start).split('.')[0]
            DASHBOARD_HTML = f"""data:text/html,<html><head>
                <style>
                    body {{ background: #050505; color: white; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }}
                    .container {{ border: 10px solid #00E5FF; padding: 60px; border-radius: 50px; background: rgba(0,229,255,0.05); box-shadow: 0 0 50px rgba(0,229,255,0.2); text-align: center; width: 80%; }}
                    h1 {{ font-size: 90px; color: #00E5FF; text-transform: uppercase; margin: 0; letter-spacing: 5px; text-shadow: 0 0 20px #00E5FF; }}
                    .stats-box {{ display: grid; grid-template-columns: 1fr; gap: 30px; margin-top: 50px; }}
                    .stat {{ font-size: 50px; background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; }}
                    .label {{ color: #FFD700; display: block; font-size: 30px; margin-bottom: 10px; }}
                    .scan {{ color: lime; font-size: 40px; margin-top: 40px; animation: pulse 1s infinite; }}
                    @keyframes pulse {{ 0%{{opacity:1;}} 50%{{opacity:0.5;}} 100%{{opacity:1;}} }}
                </style></head><body>
                <div class="container">
                    <h1>BEAST NEURAL HUB</h1>
                    <div class="stats-box">
                        <div class="stat"><span class="label">SYSTEM UPTIME</span> {uptime}</div>
                        <div class="stat"><span class="label">TOTAL PROMOTIONS</span> {total_promoted}</div>
                        <div class="stat"><span class="label">QUEUED CREATORS</span> {len(user_queue)}</div>
                    </div>
                    <div class="scan">● SEARCHING FOR NEXT CREATOR...</div>
                </div>
            </body></html>"""

            if len(user_queue) > 0:
                # 1. SHOW HUB (5s)
                driver.get(DASHBOARD_HTML)
                inject_ui(driver, "SYNCHRONIZING MATRIX", timer_sec=5, mode="HUB")
                time.sleep(5)
                
                # 2. PROMOTION (30s)
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                
                log(f"🚀 SPOTLIGHT ON: {name}")
                driver.get(url)
                time.sleep(5) 
                inject_ui(driver, f"SPOTLIGHT: {name}", timer_sec=30, mode="PROMO")
                
                total_promoted += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                
                # Cooldown Thread
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # IDLE HUB
                driver.get(DASHBOARD_HTML)
                inject_ui(driver, "NEURAL HUB IDLE", timer_sec=10, mode="HUB")
                time.sleep(10)
        except Exception as e:
            log(f"Engine Glitch: {e}")
            time.sleep(5)

# --- 4. FFmpeg BROADCAST ENGINE ---
def stream_engine():
    log("💀 Pumping 8000K Global Broadcast...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
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
