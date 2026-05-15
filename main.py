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
LIVE_VIDEO_ID = "5of2o7kJRvg" 
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Globals
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0
current_media_id = ""

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# Create a stable Lobby File
def create_lobby_file():
    html = """
    <html><body style="background:#000; color:white; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:10px solid #00E5FF; box-sizing:border-box;">
        <h1 style="font-size:70px; color:#00E5FF; text-shadow:0 0 20px #00E5FF; margin:0;">NEURAL HUB v15</h1>
        <div style="background:rgba(255,255,255,0.05); padding:30px; border-radius:20px; border:1px solid #333; margin-top:30px; text-align:center; width:80%;">
            <p style="font-size:35px; color:gold;">UPTIME: <span id="uptime">00:00:00</span></p>
            <p style="font-size:35px;">TOTAL PROMOTIONS: <span id="promo-count">0</span></p>
            <p style="font-size:30px; color:lime;">SCANNING CHAT FOR CREATORS...</p>
        </div>
    </body></html>
    """
    with open("lobby.html", "w") as f:
        f.write(html)

# --- 1. SEARCH FOR VIDEO ID ---
def get_video_id(query):
    try:
        cmd = ["yt-dlp", "--get-id", f"ytsearch1:{query}"]
        return subprocess.check_output(cmd).decode().strip()
    except: return ""

# --- 2. CHAT SNIPER ---
def chat_sniper():
    global user_queue, current_media_id
    log("💀 Sniper Matrix v15 Online...")
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
                        if vid_id: current_media_id = vid_id
                    
                    channel_url = f"https://www.youtube.com/channel/{author_id}"
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, channel_url, author_id])
                        log(f"🧬 QUEUED: {author_name}")
            time.sleep(5)
        except: time.sleep(10)

# --- 3. MASTER UI INJECTOR ---
def inject_ui(driver, title, timer_sec=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    queue_html = "".join([f"<div style='font-size:22px; margin-bottom:5px;'>- {u[0]}</div>" for u in user_queue[:4]])
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();

        // 🟢 FIX: FORCE YOUTUBE TO MOVE DOWN (LOGO PROTECTION)
        if ("{mode}" == "PROMO") {{
            var m = document.getElementById('masthead-container');
            if(m) m.style.top = "120px";
            document.body.style.marginTop = "120px";
        }}

        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; z-index:9999999; pointer-events:none; font-family:monospace;';
        
        var content = `
            <style>
                .top-bar {{ background:rgba(0,0,0,0.9); border-bottom:4px solid cyan; padding:15px; display:flex; justify-content:space-between; align-items:center; }}
                .timer {{ font-size:60px; color:yellow; font-weight:bold; margin-right:20px; }}
                .title {{ font-size:30px; color:white; font-weight:bold; text-align:left; padding-left:20px; }}
                .q-box {{ position:fixed; top:150px; left:20px; background:rgba(0,0,0,0.8); padding:15px; border-radius:10px; border-left:8px solid lime; width:300px; }}
                .media-share {{ position:fixed; bottom:120px; right:20px; width:350px; height:200px; border:4px solid gold; background:black; overflow:hidden; }}
                .footer {{ position:fixed; bottom:0; width:100%; background:red; color:white; padding:15px; text-align:center; font-size:25px; font-weight:bold; }}
            </style>
            <div class="top-bar">
                <div class="title">{title}</div>
                <div class="timer" id="b-timer">{timer_sec}s</div>
            </div>
            <div class="q-box">
                <div style="color:lime; font-weight:bold; margin-bottom:5px;">NEXT IN LINE:</div>
                {queue_html}
            </div>
            <div class="media-share" style='display:{"block" if current_media_id else "none"}'>
                <iframe src="https://www.youtube.com/embed/{current_media_id}?autoplay=1&mute=1" style="width:100%; height:100%; border:none;"></iframe>
            </div>
            <div class="footer">🚀 LIKE THE STREAM & CHAT TO JOIN! 🚀</div>
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

# --- 4. BROWSER CONTROLLER ---
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Matrix Studio Starting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com') 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    lobby_path = "file://" + os.path.abspath("lobby.html")

    while True:
        try:
            if len(user_queue) > 0:
                # Lobby Transition (5s)
                driver.get(lobby_path)
                driver.execute_script(f"document.getElementById('promo-count').innerText = '{total_promoted}';")
                inject_ui(driver, "SYSTEM RELOADING...", timer_sec=5, mode="HUB")
                time.sleep(5)
                
                # Promotion (30s)
                user = user_queue.pop(0)
                name, url, author_id = user[0], user[1], user[2]
                log(f"🌟 SPOTLIGHT: {name}")
                driver.get(url)
                time.sleep(4)
                inject_ui(driver, f"PROMOTING: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(author_id)
                time.sleep(30)
                threading.Timer(60, lambda: promoted_ids.discard(author_id)).start()
            else:
                # Idle: Show Host
                driver.get(MY_CHANNEL_URL)
                inject_ui(driver, "STATION HOST", timer_sec=10, mode="PROMO")
                time.sleep(10)
        except: time.sleep(5)

# --- 5. BROADCAST ENGINE ---
def stream_engine():
    log("💀 Pumping 6000K Zero-Latency Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-b:v", "6000k", "-maxrate", "6000k", "-bufsize", "3000k",
        "-pix_fmt", "yuv420p", "-g", "30",
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
    create_lobby_file()
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
