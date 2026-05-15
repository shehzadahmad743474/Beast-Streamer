import os
import subprocess
import threading
import time
import pytchat
import sys

# --- 💀 NAKED SECRETS 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"

# 🔴 YAHAN ASLI 11-CHARACTER VIDEO ID DAALNA (Jaise dQw4w9WgXcQ)
LIVE_VIDEO_ID = "5of2o7kJRvg" # Tere screenshot URL se nikala hai maine
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"

# Globals for Queue System
user_queue = []
current_target = "NO ONE YET"

def log(msg):
    # GitHub Actions mein logs turant dikhane ke liye flush=True zaroori hai
    print(msg, flush=True)

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

def chat_sniper():
    """Reads live chat to add users to queue"""
    global user_queue
    log(f"💀 Chat Sniper Active. Target ID: [{LIVE_VIDEO_ID}]")
    
    # Check if ID is exactly 11 characters
    if len(LIVE_VIDEO_ID) != 11:
        log("❌ FATAL ERROR: VIDEO ID MUST BE 11 CHARACTERS LONG!")
        return

    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            log("✅ Successfully hooked into YouTube Chat Matrix!")
            
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author = c.author.name
                    log(f"💬 COMMAND RECEIVED -> {author}: {c.message}")
                    
                    if author not in user_queue and author != current_target:
                        user_queue.append(author)
                        log(f"[+] Added {author}. Queue size: {len(user_queue)}")
            
            log("[-] Chat disconnected. Waiting for reconnect...")
            time.sleep(5)
        except Exception as e:
            log(f"[-] Chat Sniper Error (Is the stream Public?): {e}")
            time.sleep(5)

def stream_engine():
    """BeastGPT Dynamic Vertical Video Generator"""
    log("💀 Master Encoder Online. Generating High-End Vertical UI...")
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30",
        "-f", "lavfi", "-i", "aevalsrc=exprs=0",
        "-vf", (
            "colorchannelmixer=rr=0.1:gg=0.1:bb=0.2,"
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
