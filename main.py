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
STREAM_KEY = "m2bb-e8t6-ztt9-1fs0-8j5x" 
# 🔴 IS ID KO HAR BAAR CHANGE KARNA HAI (Dhyan se dekh URL mein)
LIVE_VIDEO_ID = "5of2o7kJRvg" 
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

# Logic Matrix
user_queue = [] 
promoted_ids = set() 
session_start = datetime.now()
total_promoted = 0
last_msg = "WAITING FOR CONNECTION..."

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# 1. GENERATE PHYSICAL LOBBY FILE (Patched for White Screen)
def create_lobby():
    html = """
    <html><body style="background:#000; color:cyan; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; border:25px solid cyan; box-sizing:border-box;">
        <h1 style="font-size:80px; text-shadow:0 0 30px cyan; margin:0; font-weight:900;">BEAST V21 HUB</h1>
        <div style="background:rgba(255,255,255,0.05); padding:40px; border-radius:30px; border:4px solid #333; margin-top:40px; text-align:center; width:90%;">
            <div style="display:flex; justify-content:space-around; width:100%;">
                <div style="font-size:35px;">PROMOTED:<br><span id="p-count" style="color:gold; font-size:60px;">0</span></div>
                <div style="font-size:35px;">IN QUEUE:<br><span id="q-count" style="color:lime; font-size:60px;">0</span></div>
            </div>
            <p style="font-size:35px; color:white; margin-top:30px; border-top:2px solid #222; padding-top:20px;">
                🧬 MATRIX STATUS: <span style="color:lime; animation:pulse 1s infinite;">ACTIVE</span>
            </p>
        </div>
        <style> @keyframes pulse { 0%{opacity:1;} 50%{opacity:0.3;} 100%{opacity:1;} } </style>
    </body></html>
    """
    with open("lobby.html", "w") as f: f.write(html)

# 2. CHAT SNIPER (V14 - DEEP SCAN & LOGGING)
def chat_sniper():
    global user_queue, last_msg
    log(f"💀 Sniper Matrix v21 Arming... Target ID: [{LIVE_VIDEO_ID}]")
    
    while True:
        try:
            # We fetch more items and bypass Top Chat
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False, topchat_only=False)
            log("✅ Successfully Synced with YouTube Live Data Stream!")
            
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author_name = c.author.name
                    author_id = c.author.channelId
                    last_msg = f"{author_name}: {c.message[:20]}"
                    log(f"💬 RECV -> {author_name}: {c.message}")
                    
                    c_url = f"https://www.youtube.com/channel/{author_id}"
                    if author_id not in promoted_ids and not any(u[2] == author_id for u in user_queue):
                        user_queue.append([author_name, c_url, author_id])
                        log(f"🧬 QUEUED: {author_name}")
            
            log("[-] Connection Dropped. Re-Syncing...")
            time.sleep(5)
        except Exception as e:
            log(f"[-] Sniper Glitch: {e}")
            time.sleep(10)

# 3. THE BEAST UI INJECTOR (v21 - PRECISE SCALING & LOGS)
def inject_ui(driver, title, timer=30, mode="PROMO"):
    uptime = str(datetime.now() - session_start).split('.')[0]
    q_html = "".join([f"<div style='margin-bottom:8px;'>• {u[0]}</div>" for u in user_queue[:5]])
    if not q_html: q_html = "Waiting for chat..."
    
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{ createHTML: (s) => s }});
        }}
        
        var ui = document.getElementById('beast-ui');
        if(ui) ui.remove();

        // 🟢 NUCLEAR LOGO FIX: PUSH 500PX
        if ("{mode}" == "PROMO") {{
            var head = document.getElementById('masthead-container');
            if(head) head.style.display = "none";
            var app = document.querySelector('ytd-app');
            if(app) app.style.marginTop = "500px";
            document.body.style.paddingTop = "500px";
            document.body.style.background = "#000";
        }}

        var container = document.createElement('div');
        container.id = 'beast-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:2147483647; pointer-events:none; font-family:Sans-Serif;';
        
        var content = `
            <style>
                .top-plate {{ background:rgba(0,0,0,0.9); border-bottom:8px solid #00E5FF; height:220px; display:flex; flex-direction:column; justify-content:center; align-items:center; }}
                .main-title {{ font-size: 5vw; color:white; font-weight:900; text-transform:uppercase; }}
                .timer-txt {{ font-size: 11vw; color:#FFFF00; font-weight:bold; }}
                .side-panel {{ position:fixed; top:250px; left:20px; background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border-left:12px solid lime; width:420px; color:white; }}
                .q-label {{ color:lime; font-size:3.5vw; font-weight:bold; margin-bottom:15px; border-bottom:2px solid #333; }}
                .q-list {{ font-size:2.8vw; line-height:1.2; font-family:monospace; }}
                .msg-log {{ position:fixed; bottom:180px; left:20px; color:cyan; font-size:2vw; background:black; padding:10px; border:1px solid #333; }}
                .footer {{ position:fixed; bottom:0; width:100%; background:linear-gradient(90deg, red, black, red); color:white; padding:30px; text-align:center; font-size:5vw; font-weight:bold; border-top:5px solid white; }}
            </style>
            <div class="top-plate">
                <div class="main-title">{title}</div>
                <div class="timer-txt" id="b-timer">{timer}s</div>
            </div>
            <div class="side-panel">
                <div class="q-label">UP NEXT:</div>
                <div class="q-list">{q_html}</div>
            </div>
            <div class="msg-log">📡 STATUS: {last_msg}</div>
            <div class="footer">🚀 LIKE THE STREAM & CHAT TO JOIN 🚀</div>
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

# 4. BROWSER HUB
def browser_controller():
    global user_queue, promoted_ids, total_promoted
    log("💀 Booting Neural Matrix v21...")
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
                inject_ui(driver, "INITIALIZING...", timer=5, mode="HUB")
                time.sleep(5)
                
                # Promotion (30s)
                u = user_queue.pop(0)
                log(f"🌟 TARGETING: {u[0]}")
                driver.get(u[1])
                time.sleep(5)
                inject_ui(driver, f"PROMOTING: {u[0]}", timer=30, mode="PROMO")
                total_promoted += 1
                promoted_ids.add(u[2])
                time.sleep(30)
                threading.Timer(60, lambda: promoted_ids.discard(u[2])).start()
            else:
                # Idle Dashboard
                driver.get(lobby_url)
                driver.execute_script(f"document.getElementById('p-count').innerText='{total_promoted}'; document.getElementById('q-count').innerText='{len(user_queue)}';")
                inject_ui(driver, "STATION IDLE", timer=10, mode="HUB")
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
