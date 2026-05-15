import os
import subprocess
import threading
import time
import sys

# --- 💀 NAKED SECRETS 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "5of2o7kJRvg" # KEEP IT UPDATED
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"

# Globals
user_queue = []
current_target = "NO ONE YET"

def log(msg):
    print(msg, flush=True)

# --- CHAT SNIPER ---
def chat_sniper():
    global user_queue
    log(f"💀 Chat Sniper V4 Active. Target ID: [{LIVE_VIDEO_ID}]")
    
    try:
        import pytchat
    except ImportError:
        log("Installing pytchat fallback...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytchat"])
        import pytchat

    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            log("✅ Connected to YouTube Chat Matrix!")
            
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author = c.author.name
                    log(f"💬 RECV -> {author}: {c.message}")
                    
                    if author not in user_queue and author != current_target:
                        user_queue.append(author)
                        log(f"[+] Added {author}. Queue size: {len(user_queue)}")
            
            log("[-] Connection lost or Chat Ended. Retrying...")
            time.sleep(10)
        except Exception as e:
            log(f"[-] Chat Sniper Error (Is Video ID Correct?): {str(e)[:50]}")
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
            time.sleep(20) 
        else:
            current_target = "WAITING FOR CHAT..."
            time.sleep(2)

def stream_engine():
    """BeastGPT Dynamic Vertical Video Generator + Synthesized Audio"""
    log("💀 Master Encoder Online. Synthesizing Local Media...")
    
    # BEAST FIX: Bypassed external MP3. Generating internal Lofi/Ambient noise.
    # aevalsrc=exprs='0.1*sin(2*PI*t*432)': Continuous 432Hz ambient frequency (No 403 possible)
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-f", "lavfi", "-i", "smptebars=size=1080x1920:rate=30",
        "-f", "lavfi", "-i", "aevalsrc=exprs='0.1*sin(2*PI*t*432)'", 
        
        "-vf", (
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
    log("=== BEASTGPT LOCAL-SYNTH MATRIX ===")
    
    open("current.txt", "w").close()
    open("queue.txt", "w").close()
    
    threading.Thread(target=update_ui_files, daemon=True).start()
    threading.Thread(target=queue_manager, daemon=True).start()
    threading.Thread(target=chat_sniper, daemon=True).start()
    
    stream_engine()
