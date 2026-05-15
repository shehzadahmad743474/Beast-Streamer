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
LIVE_VIDEO_ID = "5of2o7kJRvg" # <--- HAR BAAR CHECK KARNA
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. CHAT SNIPER (V7) ---
def chat_sniper():
    global user_queue
    log("💀 Sniper Matrix v7 Active...")
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
                        log(f"🧬 QUEUE UPDATED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. MASTER UI INJECTOR (Supports both HUB and PROMO) ---
def inject_beast_ui(driver, title, timer_sec=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    queue_html = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:5]])
    if not queue_html: queue_html = "<div class='q-item' style='color:gray'>Waiting for chat...</div>"
    
    # CSS & HTML Matrix
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-main-ui');
        if(ui) ui.remove();

        // LOGO POSITION FIX
        if ("{mode}" == "PROMO") {{
            document.body.style.paddingTop = "200px";
            document.body.style.background = "#000";
        }} else {{
            document.body.style.paddingTop = "0";
            document.body.style.background = "#050505";
        }}

        var container = document.createElement('div');
        container.id = 'beast-main-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999999; pointer-events:none; font-family:monospace;';
        
        var content = `
            <style>
                .top-bar {{ background:rgba(0,0,0,0.95); border-bottom:6px solid cyan; padding:30px; text-align:center; box-shadow:0 10px 40px rgba(0,255,255,0.3); }}
                .status-txt {{ font-size:50px; color:white; font-weight:bold; text-transform:uppercase; letter-spacing:3px; }}
                .timer-txt {{ font-size:110px; color:#FFFF00; font-weight:bold; text-shadow:0 0 20px rgba(255,255,0,0.5); }}
                .stats-panel {{ position:absolute; top:250px; left:30px; background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border-left:15px solid lime; width:450px; }}
                .st-label {{ color:lime; font-size:35px; font-weight:bold; margin-bottom:10px; }}
                .q-item {{ color:white; font-size:30px; margin-bottom:8px; border-bottom:1px solid #333; }}
                .hub-center {{ position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); text-align:center; width:90%; {"display:none;" if mode=="PROMO" else "display:block;"} }}
                .hub-title {{ font-size:100px; color:cyan; border:8px solid cyan; padding:40px; border-radius:30px; animation: glow 1s infinite alternate; }}
                .footer {{ position:absolute; bottom:0; width:100%; background:linear-gradient(90deg, #FF0000, #000, #FF0000); color:white; padding:25px; text-align:center; font-size:38px; font-weight:bold; }}
                @keyframes glow {{ from{{box-shadow:0 0 20px cyan;}} to{{box-shadow:0 0 50px cyan;}} }}
            </style>
            <div class="top-bar">
                <div class="status-txt">{title}</div>
                <div class="timer-txt" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="stats-panel">
                <div class="st-label">NEXT IN LINE:</div>
                {queue_html}
                <div style="margin-top:20px;">
                    <div class="st-label" style="color:cyan">UPTIME: {uptime}</div>
                    <div class="st-label" style="color:orange">PROMOTED: {total_promoted}</div>
                </div>
            </div>
            <div class="hub-center">
                <div class="hub-title">NEURAL HUB v13</div>
                <h2 style="font-size:50px; color:white; margin-top:40px;">SCANNING FOR NEXT CREATOR...</h2>
            </div>
            <div class="footer">🔥 SUBSCRIBE & TYPE IN CHAT TO JOIN THE QUEUE 🔥</div>
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
    except Exception as e: log(f"UI Injection Error: {e}")

# --- 3. BROWSER CONTROLLER ---
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Matrix Studio Starting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com') 
    opts.add_argument('--force-dark-mode')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    while True:
        try:
            if len(user_queue) > 0:
                # TRANSITION (5s)
                driver.get("about:blank") # Clean slate to avoid white screen
                inject_beast_ui(driver, "SYNCHRONIZING HUB", timer_sec=5, mode="HUB")
                time.sleep(5)
                
                # PROMOTION (30s)
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                
                log(f"🌟 SPOTLIGHT: {name}")
                driver.get(url)
                time.sleep(5) # Wait for load
                inject_beast_ui(driver, f"COMMUNITY SPOTLIGHT: {name}", timer_sec=30, mode="PROMO")
                
                total_promoted += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                
                # 1 Minute Cooldown
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # IDLE HUB (Always show dashboard when queue empty)
                driver.get("about:blank")
                inject_beast_ui(driver, "STATION IDLE", timer_sec=10, mode="HUB")
                time.sleep(10)
        except Exception as e:
            log(f"Controller Glitch: {e}")
            time.sleep(5)

# --- 4. BROADCAST ENGINE ---
def stream_engine():
    log("💀 Pumping 8000K Bitrate to Worldwide Feed...")
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
