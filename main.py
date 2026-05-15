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

# Matrix Logic
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0
current_media_id = ""

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# 1. GENERATE PHYSICAL LOBBY FILE
def create_lobby():
    html = """
    <html><body style="background:#000; color:cyan; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:20px solid #00E5FF; box-sizing:border-box;">
        <h1 style="font-size:75px; text-shadow:0 0 30px cyan; margin:0; font-weight:900;">NEURAL STATION v20</h1>
        <div style="background:rgba(255,255,255,0.05); padding:50px; border-radius:40px; border:4px solid #333; margin-top:40px; text-align:center; width:85%;">
            <div style="display:flex; justify-content:space-around; width:100%;">
                <div style="font-size:30px;">PROMOTED:<br><span id="p-count" style="color:gold; font-size:55px;">0</span></div>
                <div style="font-size:30px;">IN QUEUE:<br><span id="q-count" style="color:lime; font-size:55px;">0</span></div>
            </div>
            <p style="font-size:30px; color:white; margin-top:40px; border-top:1px solid #222; padding-top:25px;">🧬 SYSTEM STATUS: <span style="color:lime;">SCANNING CHAT...</span></p>
        </div>
    </body></html>
    """
    with open("lobby.html", "w") as f: f.write(html)

# 2. CHAT SNIPER (V13 - COMMANDS)
def chat_sniper():
    global user_queue, current_media_id
    log("💀 Sniper Matrix v20 Armed...")
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
                        log(f"🧬 QUEUED: {author_name}")
            time.sleep(5)
        except: time.sleep(10)

# 3. THE BEAST UI INJECTOR (v20 - SLEEK & LOGO SAFE)
def inject_ui(driver, title, timer=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    q_html = "".join([f"<div style='margin-bottom:6px;'>• {u[0]}</div>" for u in user_queue[:5]])
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();

        // 🟢 ULTIMATE LOGO FIX: PUSH CONTENT DOWN 550PX
        if ("{mode}" == "PROMO") {{
            var head = document.getElementById('masthead-container');
            if(head) head.remove(); 
            var page = document.querySelector('ytd-app');
            if(page) {{
                page.style.marginTop = "550px";
                page.style.backgroundColor = "black";
            }}
            document.body.style.paddingTop = "550px";
            document.body.style.backgroundColor = "black";
        }}

        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:2147483647; pointer-events:none; font-family:Sans-Serif;';
        
        var content = `
            <style>
                .top-bar {{ background:rgba(0,0,0,0.95); border-bottom:6px solid #00E5FF; height:180px; display:flex; justify-content:space-between; align-items:center; padding: 0 40px; box-shadow:0 10px 40px rgba(0,255,255,0.4); }}
                .status-txt {{ font-size:4vw; color:white; font-weight:bold; text-transform:uppercase; }}
                .timer-txt {{ font-size:10vw; color:#FFFF00; font-weight:bold; font-family:monospace; }}
                .side-panel {{ position:fixed; top:600px; left:20px; background:rgba(0,0,0,0.9); padding:25px; border-radius:20px; border-left:12px solid lime; width:380px; color:white; }}
                .q-label {{ color:lime; font-size:3vw; font-weight:bold; margin-bottom:10px; border-bottom:2px solid #333; }}
                .q-list {{ font-size:2.5vw; line-height:1.2; font-family:monospace; }}
                .media-share {{ position:fixed; bottom:180px; right:20px; width:450px; height:260px; background:black; border:5px solid gold; border-radius:20px; overflow:hidden; pointer-events:auto; }}
                .footer {{ position:fixed; bottom:0; width:100%; background:linear-gradient(90deg, #F00, #000, #F00); color:white; padding:25px; text-align:center; font-size:3.5vw; font-weight:bold; border-top:4px solid white; }}
            </style>
            <div class="top-bar">
                <div class="status-txt">{title}</div>
                <div class="timer-txt" id="b-timer">{timer}s</div>
            </div>
            <div class="side-panel">
                <div class="q-label">NEXT:</div>
                <div class="q-list">{q_html}</div>
                <div style="margin-top:15px; color:cyan; font-size:2vw;">SESSION: {uptime}</div>
            </div>
            <div class="media-share" id="media-box" style='display:{"block" if current_media_id else "none"}'>
                <div style="background:gold; color:black; font-weight:bold; padding:3px; font-size:1.5vw; text-align:center;">MEDIA PLAYER</div>
                <iframe src="https://www.youtube.com/embed/{current_media_id}?autoplay=1&mute=1&controls=0" style="width:100%; height:85%; border:none;"></iframe>
            </div>
            <div class="footer">🚀 LIKE THE STREAM TO STAY IN QUEUE! 🚀</div>
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
    log("💀 Launching Neural Hub v20...")
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
                
                # Promotion (30s)
                u = user_queue.pop(0)
                log(f"🌟 SPOTLIGHT: {u[0]}")
                driver.get(u[1])
                time.sleep(5)
                inject_ui(driver, f"PROMOTING: {u[0]}", timer=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(u[2])
                time.sleep(30)
                # 60s cooldown
                threading.Timer(60, lambda: promoted_ids.discard(u[2])).start()
            else:
                # Idle Dashboard
                driver.get(lobby_url)
                driver.execute_script(f"document.getElementById('p-count').innerText='{total_promoted}'; document.getElementById('q-count').innerText='{len(user_queue)}';")
                inject_ui(driver, "SYSTEM IDLE", timer=10, mode="HUB")
                time.sleep(10)
        except: time.sleep(5)

# 5. STREAM ENGINE
def stream_engine():
    log("💀 Pumping 8000K Worldwide Feed...")
    ffmpeg_cmd = [
        "ffmpeg", "-loglevel", "error", "-re",
        "-f", "x11grab", "-video_size", "1080x1920", "-i", ":99.0", 
        "-stream_loop", "-1", "-i", "bgm.mp3",                      
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-b:v", "8000k", "-maxrate", "8000k", "-bufsize", "4000k",
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
