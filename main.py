import os
import subprocess
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytchat

# --- 💀 NAKED HARDCODED CONFIG 💀 ---
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

# 1. GENERATE PHYSICAL LOBBY FILE (Anti-White Screen)
def create_lobby():
    html = """
    <html><body style="background:#000; color:cyan; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:30px solid cyan; box-sizing:border-box; overflow:hidden;">
        <h1 style="font-size:120px; text-shadow:0 0 40px cyan; margin:0; font-weight:900;">BEAST HUB v17</h1>
        <div style="background:rgba(0,255,255,0.1); padding:60px; border-radius:40px; border:5px solid white; margin-top:50px; text-align:center; width:90%;">
            <p style="font-size:60px; color:yellow; margin:10px;">SYSTEM STATUS: <span style="color:lime;">ONLINE</span></p>
            <p style="font-size:50px; color:white; margin:10px;">SCANNING CHAT FOR NEXT CREATOR...</p>
            <hr style="border:1px solid #333; margin:40px 0;">
            <div style="display:flex; justify-content:space-around; width:100%;">
                <div style="font-size:40px;">PROMOTED:<br><span id="p-count" style="color:cyan; font-size:60px;">0</span></div>
                <div style="font-size:40px;">QUEUED:<br><span id="q-count" style="color:cyan; font-size:60px;">0</span></div>
            </div>
        </div>
    </body></html>
    """
    with open("lobby.html", "w") as f: f.write(html)

# 2. CHAT SNIPER (V10 - RECOVERY MODE)
def chat_sniper():
    global user_queue, current_media_id
    log("💀 Sniper Matrix v17 Arming...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    msg = c.message
                    author_name = c.author.name
                    author_id = c.author.channelId
                    
                    if "!play " in msg:
                        q = msg.split("!play ")[1].strip()
                        try:
                            v_id = subprocess.check_output(["yt-dlp", "--get-id", f"ytsearch1:{q}"]).decode().strip()
                            if v_id: current_media_id = v_id
                        except: pass
                    
                    c_url = f"https://www.youtube.com/channel/{author_id}"
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, c_url, author_id])
                        log(f"🧬 DETECTED: {author_name}")
            time.sleep(5)
        except: time.sleep(10)

# 3. BEAST UI OVERLAY (v17 - MEGA SIZE)
def inject_ui(driver, title, timer=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    q_html = "".join([f"<div style='margin-bottom:10px;'>⚡ {u[0]}</div>" for u in user_queue[:5]])
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();

        // 🟢 NUCLEAR LOGO FIX
        if ("{mode}" == "PROMO") {{
            var head = document.getElementById('masthead-container');
            if(head) head.style.display = "none";
            var page = document.querySelector('ytd-app');
            if(page) page.style.marginTop = "450px";
            document.body.style.background = "#000";
        }}

        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:2147483647; pointer-events:none; font-family:monospace;';
        
        var content = `
            <style>
                .top-plate {{ background:rgba(0,0,0,0.95); border-bottom:10px solid #00E5FF; height:350px; display:flex; flex-direction:column; justify-content:center; align-items:center; }}
                .main-title {{ font-size: 7vw; color:white; font-weight:900; text-transform:uppercase; text-shadow: 0 0 30px cyan; }}
                .timer-txt {{ font-size: 15vw; color:#FFFF00; font-weight:bold; line-height:1; }}
                .side-panel {{ position:fixed; top:400px; left:20px; background:rgba(0,0,0,0.9); padding:40px; border-radius:30px; border-left:20px solid lime; width:500px; color:white; }}
                .q-label {{ color:lime; font-size:5vw; font-weight:bold; border-bottom:4px solid #333; margin-bottom:20px; }}
                .q-list {{ font-size:4vw; line-height:1.2; }}
                .media-box {{ position:fixed; bottom:250px; right:20px; width:550px; height:350px; background:black; border:10px solid gold; border-radius:30px; overflow:hidden; display:{"block" if current_media_id else "none"}; }}
                .footer-neon {{ position:fixed; bottom:0; width:100%; background:linear-gradient(90deg, #F00, #000, #F00); color:white; padding:40px; text-align:center; font-size:6vw; font-weight:bold; border-top:8px solid white; }}
            </style>
            <div class="top-plate">
                <div class="main-title">{title}</div>
                <div class="timer-txt" id="b-timer">{timer}s</div>
            </div>
            <div class="side-panel">
                <div class="q-label">UP NEXT:</div>
                <div class="q-list">{q_html}</div>
            </div>
            <div class="media-box">
                <iframe src="https://www.youtube.com/embed/{current_media_id}?autoplay=1&mute=1" style="width:100%; height:100%; border:none;"></iframe>
            </div>
            <div class="footer-neon">🔥 LIKE THE STREAM TO JOIN 🔥</div>
        `;
        container.innerHTML = window.beastPolicy ? window.beastPolicy.createHTML(content) : content;
        document.body.appendChild(container);

        var s = {timer};
        var itv = setInterval(function() {{
            s--;
            var d = document.getElementById('b-timer');
            if(d) d.innerText = s + "s";
            if(s <= 0) clearInterval(itv);
        }}, 1000);
    }})();
    """
    try: driver.execute_script(ui_script)
    except: pass

# 4. BROWSER CONTROLLER
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Booting Neural Chrome...")
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--app=https://www.youtube.com')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    lobby_url = "file://" + os.path.abspath("lobby.html")

    while True:
        try:
            if len(user_queue) > 0:
                # Lobby (5s)
                driver.get(lobby_url)
                driver.execute_script(f"document.getElementById('p-count').innerText='{total_promoted}'; document.getElementById('q-count').innerText='{len(user_queue)}';")
                inject_ui(driver, "NEXT CREATOR...", timer=5, mode="HUB")
                time.sleep(5)
                
                # Promo (30s)
                u = user_queue.pop(0)
                log(f"🚀 SPOTLIGHT: {u[0]}")
                driver.get(u[1])
                time.sleep(5)
                inject_ui(driver, f"USER: {u[0]}", timer=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(u[2])
                time.sleep(30)
                threading.Timer(60, lambda: promoted_ids.discard(u[2])).start()
            else:
                driver.get(lobby_url)
                inject_ui(driver, "STATION IDLE", timer=10, mode="HUB")
                time.sleep(10)
        except: time.sleep(5)

# 5. STREAM ENGINE
def stream_engine():
    log("💀 Pumping 8000K Zero-Latency Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "3000k",
        "-pix_fmt", "yuv420p", "-g", "60",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-map", "0:v", "-map", "1:a", "-f", "flv", f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]
    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            time.sleep(2)
        except: pass

if __name__ == "__main__":
    create_lobby()
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
