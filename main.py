import os
import subprocess
import threading
import time
import sys

# --- 💀 NAKED SECRETS 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # CHANGE THIS IF YOU START A NEW STREAM!
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"

# BEASTGPT AUDIO INJECTION: Direct link to a NoCopyright mp3
# Ye link hamesha chalti hai aur FFmpeg isko loop karega
BGM_AUDIO_URL = "https://www.bensound.com/bensound-music/bensound-actionable.mp3"

# Globals
user_queue = []
current_target = "NO ONE YET"

def log(msg):
    print(msg, flush=True)

# --- THE CHAT SNIPER (V3 - PYTCHAT BYPASS) ---
# Hum ek alternate library use kar rahe hain jo Studio/Public dono chat padhti hai
def chat_sniper():
    global user_queue
    log(f"💀 Chat Sniper V3 Active. Target ID: [{LIVE_VIDEO_ID}]")
    
    try:
        import pytchat
    except:
        log("Installing pytchat fallback...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytchat"])
        import pytchat

    while True:
        try:
            # Adding topchat_only=False ensures it reads all messages, not just "Top"
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False, topchat_only=False)
            log("✅ Connected to YouTube Chat Matrix!")
            
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author = c.author.name
                    log(f"💬 RECV -> {author}: {c.message}")
                    
                    if author not in user_queue and author != current_target:
                        user_queue.append(author)
                        log(f"[+] Added {author}. Queue size: {len(user_queue)}")
            
            log("[-] Connection lost. YouTube might be blocking the IP. Retrying...")
            time.sleep(10)
        except Exception as e:
            log(f"[-] Fatal Sniper Error: {e}")
            time.sleep(15)

def update_ui_files():
    """Generates clean text files for FFmpeg to read"""
    while True:
        try:
            with open("current.txt", "w", encoding="utf-8") as f:
                f.write(f"PROMOTING NOW:\n\n{current_target.upper()}")
            
            q_text = "NEXT IN LINE:\n"
            q_text += "----------------------\n"
            if len(user_queue) == 0:
                q_text += "TYPE ANYTHING IN CHAT TO JOIN!"
            else:
                for i, u in enumerate(user_queue[:6]):
                    q_text += f"{i+1}. {u}\n"
            
            with open("queue.txt", "w", encoding="utf-8") as f:
                f.write(q_text)
                
            time.sleep(1)
        except Exception as e:
            pass

def queue_manager():
    """Handles the promotion rotation"""
    global current_target, user_queue
    while True:
        if len(user_queue) > 0:
            current_target = user_queue.pop(0)
            log(f"[*] Now Promoting: {current_target}")
            time.sleep(20) # 20 seconds spotlight
        else:
            current_target = "WAITING FOR CHAT..."
            time.sleep(2)

def stream_engine():
    """BeastGPT Dynamic Vertical Video Generator + BGM Audio"""
    log("💀 Master Encoder Online. Generating Video & Audio UI...")
    
    # FFmpeg Magic:
    # 1. Video: Animated Color background
    # 2. Audio: Loop the external BGM_AUDIO_URL infinitely
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        # 1. Background Video Input (Animated colors instead of plain black)
        "-f", "lavfi", "-i", "smptebars=size=1080x1920:rate=30",
        
        # 2. Background Audio Input (Looped external MP3)
        "-stream_loop", "-1", "-i", BGM_AUDIO_URL,
        
        "-vf", (
            # Dim the background and make it look cool
            "colorchannelmixer=rr=0.2:gg=0.2:bb=0.3,"
            "drawtext=text='CHANNEL PROMOTION STATION':fontcolor=00FF00:fontsize=65:x=(w-tw)/2:y=100:box=1:boxcolor=black@0.9:boxborderw=20,"
            "drawtext=textfile='current.txt':reload=1:fontcolor=cyan:fontsize=80:x=(w-tw)/2:y=600:box=1:boxcolor=black@0.8:boxborderw=20:line_spacing=20:text_align=C,"
            "drawtext=textfile='queue.txt':reload=1:fontcolor=white:fontsize=50:x=100:y=1200:box=1:boxcolor=black@0.7:boxborderw=15:line_spacing=10,"
            "drawtext=text='SUBSCRIBE & TYPE IN CHAT TO GET PROMOTED!':fontcolor=yellow:fontsize=45:x=(w-tw)/2:y=1750:box=1:boxcolor=black@0.8:boxborderw=10"
        ),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "2000k",
        "-maxrate", "2000k",
        "-bufsize", "4000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        
        # Audio mapping
        "-map", "0:v", "-map", "1:a",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        
        "-f", "flv",
        f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ]

    while True:
        try:
            subprocess.run(ffmpeg_cmd)
            log("[!] Stream Drop. Restarting Engine...")
            time.sleep(3)
        except:
            time.sleep(3)

if __name__ == "__main__":
    log("=== BEASTGPT SHORT-LIVE MATRIX ===")
    
    open("current.txt", "w").close()
    open("queue.txt", "w").close()
    
    threading.Thread(target=update_ui_files, daemon=True).start()
    threading.Thread(target=queue_manager, daemon=True).start()
    threading.Thread(target=chat_sniper, daemon=True).start()
    
    stream_engine()
