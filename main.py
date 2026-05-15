import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat
import json

# --- 💀 PRO STATION CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6" # <--- APNI NAYI KEY YAHAN DAALNA
LIVE_VIDEO_ID = "5of2o7kJRvg" # <--- HAR STREAM PAR YE ID CHECK KARO!
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Data Matrix
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0
current_media_id = "" # For !play command

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. SEARCH FOR VIDEO ID (!play command) ---
def get_video_id(query):
    try:
        cmd = ["yt-dlp", "--get-id", f"ytsearch1:{query}"]
        result = subprocess.check_output(cmd).decode().strip()
        return result
    except:
        return ""

# --- 2. CHAT SNIPER (V8 - COMMANDS ADDED) ---
def chat_sniper():
    global user_queue, current_media_id
    log("💀 Neural Sniper Matrix v8 Online...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    msg = c.message
                    author_name = c.author.name
                    author_id = c.author.channelId
                    
                    # Command: !play
                    if msg.startswith("!play "):
                        query = msg.replace("!play ", "").strip()
                        log(f"🎵 Media Request: {query}")
                        vid_id = get_video_id(query)
                        if vid_id:
                            current_media_id = vid_id
                            log(f"✅ Playing Media ID: {vid_id}")
                    
                    # Normal Queue Entry
                    channel_url = f"https://www.youtube.com/channel/{author_id}"
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, channel_url, author_id])
                        log(f"🧬 QUEUED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 3. MASTER UI INJECTOR (v14) ---
def inject_beast_ui(driver, title, timer_sec=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    queue_html = "".join([f"<div class='q-item'>{u[0]}</div>" for u in user_queue[:5]])
    if not queue_html: queue_html = "<div class='q-item' style='color:gray'>Join the chat to start...</div>"
    
    media_share_html = ""
    if current_media_id:
        media_share_html = f'<iframe src="https://www.youtube.com/embed/{current_media_id}?autoplay=1&mute=1&controls=0" style="width:100%; height:100%; border:none;"></iframe>'

    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-main-ui');
        if(ui) ui.remove();

        // AGGRESSIVE LOGO PADDING (300px)
        if ("{mode}" == "PROMO") {{
            document.body.style.paddingTop = "300px";
            document.body.style.background = "#000";
        }}

        var container = document.createElement('div');
        container.id = 'beast-main-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999999; pointer-events:none; font-family:monospace;';
        
        var content = `
            <style>
                .top-bar {{ background:rgba(0,0,0,0.9); border-bottom:6px solid #00E5FF; padding:35px; text-align:center; box-shadow:0 10px 40px rgba(0,255,255,0.4); }}
                .status-txt {{ font-size:45px; color:white; font-weight:bold; text-transform:uppercase; }}
                .timer-txt {{ font-size:100px; color:#FFFF00; font-weight:bold; }}
                .stats-panel {{ position:absolute; top:400px; left:30px; background:rgba(0,0,0,0.85); padding:25px; border-radius:15px; border-left:12px solid lime; width:420px; }}
                .st-label {{ color:lime; font-size:32px; font-weight:bold; margin-bottom:10px; }}
                .q-item {{ color:white; font-size:28px; margin-bottom:8px; border-bottom:1px solid #333; }}
                .media-box {{ position:absolute; bottom:250px; right:30px; width:450px; height:250px; background:black; border:5px solid gold; border-radius:15px; overflow:hidden; display:{"block" if current_media_id else "none"}; }}
                .footer {{ position:absolute; bottom:0; width:100%; background:linear-gradient(90deg, #FF0000, #000, #FF0000); color:white; padding:30px; text-align:center; font-size:40px; font-weight:bold; }}
            </style>
            <div class="top-bar">
                <div class="status-txt">{title}</div>
                <div class="timer-txt" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="stats-panel">
                <div class="st-label">QUEUE LIST:</div>
                {queue_html}
                <div style="margin-top:20px; color:cyan; font-size:25px;">UPTIME: {uptime}</div>
            </div>
            <div class="media-box">
                <div style="background:gold; color:black; font-weight:bold; padding:5px; font-size:20px; text-align:center;">MEDIA SHARE</div>
                {media_share_html}
            </div>
            <div class="footer">🚀 LIKE THE STREAM & USE !play <title> 🚀</div>
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

# --- 4. THE MASTER CONTROLLER ---
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
                # Promotion Mode
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                log(f"🌟 PROMOTING: {name}")
                driver.get(url)
                time.sleep(5) 
                inject_beast_ui(driver, f"PROMOTING: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # Hub Mode
                driver.get("about:blank")
                inject_beast_ui(driver, "STATION IDLE", timer_sec=10, mode="HUB")
                time.sleep(10)
        except Exception as e:
            time.sleep(5)

# --- 5. BROADCAST ENGINE (ZERO LATENCY) ---
def stream_engine():
    log("💀 Pumping 8000K Zero-Latency Global Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast",
        "-tune", "zerolatency", # BEAST FIX: Reduces lag significantly
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "4000k", # Fast buffer
        "-pix_fmt", "yuv420p", "-g", "30", # Faster keyframes
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-map", "0:v", "-map", "1:a", "-f", "flv",
        f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]
    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            time.sleep(2)
        except: pass

if __name__ == "__main__":
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
