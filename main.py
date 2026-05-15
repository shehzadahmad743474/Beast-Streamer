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
STREAM_KEY = "hjke-9tf7-69sj-89gk-aatz" # Teri key maine repair kar di hai
LIVE_VIDEO_ID = "5of2o7kJRvg" # ISKO HAR BAAR CHECK KARNA
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
MY_CHANNEL_URL = "https://www.youtube.com/@SHEHZAD_PLAYZ"

user_queue = [] 
cooldowns = {}
total_promoted = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# --- 1. CHAT SNIPER (Stable Matrix) ---
def chat_sniper():
    global user_queue, cooldowns
    log("💀 Sniper Matrix Booting...")
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
                        log(f"⚡ QUEUED: {author_name}")
            time.sleep(5)
        except:
            time.sleep(10)

# --- 2. THE CYBERPUNK OVERLAY (BYPASSING GOOGLE SECURITY) ---
def inject_beast_ui(driver, title, timer_sec=30, mode="PROMO"):
    queue_html = "".join([f"<div style='color:white; font-size:30px; margin-bottom:5px;'>{u[0]}</div>" for u in user_queue[:5]])
    
    # BEAST BYPASS: Creating a TrustedHTML policy to kill the 'innerHTML' error
    ui_script = f"""
    (function() {{
        if (window.trustedTypes && window.trustedTypes.createPolicy && !window.beastPolicy) {{
            window.beastPolicy = window.trustedTypes.createPolicy('beastPolicy', {{
                createHTML: (string) => string
            }});
        }}
        
        var ui = document.getElementById('beast-matrix-ui');
        if(ui) ui.remove();
        
        var container = document.createElement('div');
        container.id = 'beast-matrix-ui';
        container.style = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999999; pointer-events:none; font-family:monospace; border: 25px solid {"#00ffff" if mode=="PROMO" else "#ff00ff"}; box-sizing:border-box; background:rgba(0,0,0,0.05);';
        
        var content = `
            <div style="background:black; border-bottom:5px solid cyan; padding:30px; text-align:center;">
                <div style="font-size:60px; color:#00ffff; font-weight:bold; text-shadow:0 0 20px cyan;">{title}</div>
                <div id="beast-timer" style="font-size:100px; color:#ffff00; margin-top:10px;">{timer_sec}s</div>
            </div>
            <div style="position:absolute; bottom:200px; left:40px; background:rgba(0,0,0,0.9); padding:30px; border-left:15px solid lime; width:500px; border-radius:0 20px 20px 0;">
                <div style="color:lime; font-size:40px; margin-bottom:10px; font-weight:bold;">NEXT TARGETS:</div>
                {queue_html}
            </div>
            <div style="position:absolute; bottom:50px; width:100%; text-align:center; color:white; font-size:45px; font-weight:bold; text-shadow:0 0 15px red;">🚀 SUBSCRIBE & CHAT TO JOIN 🚀</div>
        `;

        if (window.beastPolicy) {{
            container.innerHTML = window.beastPolicy.createHTML(content);
        }} else {{
            container.innerHTML = content;
        }}
        
        document.body.appendChild(container);

        var timeLeft = {timer_sec};
        var timerInterval = setInterval(function() {{
            timeLeft--;
            var tDisplay = document.getElementById('beast-timer');
            if(tDisplay) tDisplay.innerText = timeLeft + "s";
            if(timeLeft <= 0) clearInterval(timerInterval);
        }}, 1000);
    }})();
    """
    try:
        driver.execute_script(ui_script)
    except Exception as e:
        log(f"UI Injection Glitch: {e}")

# --- 3. MASTER CONTROLLER ---
def browser_controller():
    global user_queue, cooldowns, total_promoted
    log("💀 Matrix Browser Booting...")
    
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1080,1920')
    opts.add_argument('--kiosk')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    # Bypassing the Trusted Types via flags as well
    opts.add_argument('--disable-features=TrustedTypes-for-Elements,TrustedTypes')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    DASHBOARD_URL = "data:text/html,<html><body style='background:#000; color:lime; font-family:monospace; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; height:100vh; margin:0;'> <h1 style='font-size:120px; border:10px solid lime; padding:50px; box-shadow:0 0 30px lime;'>BEAST STATION v10</h1> <h2 style='font-size:70px; color:cyan; margin-top:30px;'>INITIALIZING NEXT COMMAND...</h2> </body></html>"

    while True:
        try:
            if len(user_queue) > 0:
                # Transition
                driver.get(DASHBOARD_URL)
                inject_beast_ui(driver, "SYSTEM RELOADING", timer_sec=5, mode="HOME")
                time.sleep(5)
                
                # Promotion
                name, url = user_queue.pop(0)
                log(f"🔥 INJECTING: {name}")
                driver.get(url)
                time.sleep(5) # Give YouTube time to load
                inject_beast_ui(driver, f"TARGET: {name}", timer_sec=30, mode="PROMO")
                total_promoted += 1
                cooldowns[url] = time.time()
                time.sleep(30)
            else:
                if driver.current_url != MY_CHANNEL_URL:
                    driver.get(MY_CHANNEL_URL)
                    inject_beast_ui(driver, "MASTER CHANNEL", timer_sec=10, mode="HOME")
                time.sleep(5)
        except Exception as e:
            log(f"Browser Loop Error: {e}")
            time.sleep(5)

# --- 4. FFmpeg OVERDRIVE ENGINE ---
def stream_engine():
    log("💀 Pumping 8000K Max Bitrate...")
    ffmpeg_cmd = [
        "ffmpeg", "-re",
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
        except:
            time.sleep(3)

if __name__ == "__main__":
    threading.Thread(target=chat_sniper, daemon=True).start()
    threading.Thread(target=browser_controller, daemon=True).start()
    time.sleep(15)
    stream_engine()
