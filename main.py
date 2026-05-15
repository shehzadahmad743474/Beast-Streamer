import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 ABSOLUTE HARDCODED CONFIG 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" 
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Logic Matrix
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0
current_media_id = ""

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. SEARCH FOR VIDEO ID ---
def get_video_id(query):
    try:
        # Beast Search Bypass
        cmd = ["yt-dlp", "--get-id", f"ytsearch1:{query}"]
        return subprocess.check_output(cmd).decode().strip()
    except: return ""

# --- 2. CHAT SNIPER (V9 - HIGH PRECISION) ---
def chat_sniper():
    global user_queue, current_media_id
    log("💀 Sniper Matrix v16 Online...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    msg = c.message
                    author_name = c.author.name
                    author_id = c.author.channelId
                    
                    if msg.startswith("!play "):
                        query = msg.replace("!play ", "").strip()
                        vid_id = get_video_id(query)
                        if vid_id: 
                            current_media_id = vid_id
                            log(f"🎵 Media Injected: {vid_id}")
                    
                    c_url = f"https://www.youtube.com/channel/{author_id}"
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, c_url, author_id])
                        log(f"🧬 QUEUE: {author_name}")
            time.sleep(5)
        except: time.sleep(10)

# --- 3. THE BEAST UI INJECTOR (v16 - MEGA FONTS) ---
def inject_beast_ui(driver, title, timer_sec=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    q_html = "".join([f"<div style='margin-bottom:10px;'>• {u[0]}</div>" for u in user_queue[:5]])
    if not q_html: q_html = "Waiting for chat..."
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-v16-ui');
        if(ui) ui.remove();

        // 🟢 NUCLEAR LOGO FIX: Kill YouTube Header and Push Page Down
        if ("{mode}" == "PROMO") {{
            var head = document.getElementById('masthead-container');
            if(head) head.remove();
            var app = document.querySelector('ytd-app');
            if(app) app.style.marginTop = "350px";
            document.body.style.paddingTop = "350px";
        }}

        var container = document.createElement('div');
        container.id = 'beast-v16-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:2147483647; pointer-events:none; font-family:Arial, sans-serif;';
        
        var content = `
            <style>
                .top-plate {{ background:rgba(0,0,0,0.95); border-bottom:8px solid #00E5FF; height:250px; display:flex; flex-direction:column; justify-content:center; align-items:center; box-shadow:0 15px 50px rgba(0,255,255,0.5); }}
                .main-title {{ font-size: 6vw; color:white; font-weight:900; text-transform:uppercase; text-shadow: 0 0 20px cyan; }}
                .timer-big {{ font-size: 12vw; color:#FFFF00; font-weight:bold; line-height:1; }}
                .side-panel {{ position:fixed; top:300px; left:20px; background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border-left:15px solid lime; width:450px; color:white; }}
                .q-title {{ color:lime; font-size:4vw; font-weight:bold; margin-bottom:15px; border-bottom:2px solid #333; }}
                .q-list {{ font-size:3vw; line-height:1.4; font-family:monospace; }}
                .media-share {{ position:fixed; bottom:200px; right:20px; width:500px; height:300px; background:black; border:8px solid gold; border-radius:20px; overflow:hidden; display:{"block" if current_media_id else "none"}; }}
                .footer-neon {{ position:fixed; bottom:0; width:100%; background:linear-gradient(90deg, red, #300, red); color:white; padding:30px; text-align:center; font-size:5vw; font-weight:bold; border-top:5px solid white; }}
            </style>
            <div class="top-plate">
                <div class="main-title">{title}</div>
                <div class="timer-big" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="side-panel">
                <div class="q-title">QUEUED:</div>
                <div class="q-list">{q_html}</div>
                <div style="margin-top:20px; color:cyan; font-size:2.5vw;">UPTIME: {uptime}</div>
            </div>
            <div class="media-share">
                <div style="background:gold; color:black; font-weight:bold; padding:5px; font-size:2vw; text-align:center;">LIVE MEDIA</div>
                <iframe src="https://www.youtube.com/embed/{current_media_id}?autoplay=1&mute=1&enablejsapi=1" style="width:100%; height:80%; border:none;"></iframe>
            </div>
            <div class="footer-neon">🔥 LIKE THE STREAM TO JOIN 🔥</div>
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

# --- 4. BROWSER HUB ---
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Master Studio v16 Launching...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com') 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    # NEURAL HUB PAGE
    HUB_HTML = "data:text/html,<html><body style='background:#000; color:cyan; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:20px solid cyan;'> <h1 style='font-size:10vw; text-shadow:0 0 30px cyan;'>NEURAL HUB</h1> <div style='font-size:5vw; color:white; border:5px solid white; padding:30px; border-radius:20px;'> READY FOR INJECTION </div> <h2 style='font-size:4vw; color:lime; margin-top:40px;'>SCANNING CHAT...</h2> </body></html>"

    while True:
        try:
            if len(user_queue) > 0:
                # 1. Show Hub (5s)
                driver.get(HUB_HTML)
                inject_beast_ui(driver, "SYSTEM LOADING", timer_sec=5, mode="HUB")
                time.sleep(5)
                
                # 2. Show User (30s)
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                log(f"🌟 SPOTLIGHT: {name}")
                driver.get(url)
                time.sleep(5) 
                inject_beast_ui(driver, f"PROMOTING: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # Idle Hub
                driver.get(HUB_HTML)
                inject_beast_ui(driver, "STATION IDLE", timer_sec=10, mode="HUB")
                time.sleep(10)
        except: time.sleep(5)

# --- 5. BROADCAST ---
def stream_engine():
    log("💀 Pumping 6000K Global Stream...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-b:v", "6000k", "-maxrate", "6000k", "-bufsize", "3000k",
        "-pix_fmt", "yuv420p", "-g", "60",
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
