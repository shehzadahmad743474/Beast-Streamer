import os
import subprocess
import threading
import time
import pytchat

# --- 💀 NAKED SECRETS 💀 ---
STREAM_KEY = "pv92-p957-980h-3zpy-a5p6"
LIVE_VIDEO_ID = "owsv6D0MvnBNcFLZ"
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"

# Globals for Queue System
user_queue = []
current_target = "NO ONE YET"

def update_ui_files():
    """Generates clean text files for FFmpeg to read"""
    while True:
        try:
            # Current Target (Big Text)
            with open("current.txt", "w", encoding="utf-8") as f:
                f.write(f"PROMOTING NOW:\n\n{current_target.upper()}")
            
            # Queue List
            q_text = "NEXT IN LINE:\n"
            q_text += "----------------------\n"
            if len(user_queue) == 0:
                q_text += "TYPE ANYTHING TO JOIN!"
            else:
                for i, u in enumerate(user_queue[:6]): # Show top 6
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
            print(f"[*] Now Promoting: {current_target}")
            time.sleep(30) # 30 seconds spotlight
        else:
            current_target = "WAITING FOR CHAT..."
            time.sleep(5)

def chat_sniper():
    """Reads live chat to add users to queue"""
    global user_queue
    print("💀 Chat Sniper Active. Monitoring Live Chat...")
    while True:
        try:
            # Interruptable=False prevents thread crash
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author = c.author.name
                    print(f"💬 {author}: {c.message}")
                    
                    if author not in user_queue and author != current_target:
                        user_queue.append(author)
                        print(f"[+] Added {author}. Queue: {len(user_queue)}")
        except Exception as e:
            print(f"[-] Chat Disconnected. Retrying... {e}")
            time.sleep(10)

def stream_engine():
    """BeastGPT Dynamic Vertical Video Generator"""
    print("💀 Master Encoder Online. Generating High-End Vertical UI...")
    
    # 1. Virtual Background: Gradient testsrc creates a moving background
    # 2. Scale: 1080x1920 (Vertical for Shorts Feed)
    # 3. Clean Text Overlays without Emojis to prevent box errors
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        # Animated background generation (no downloads needed)
        "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30",
        "-f", "lavfi", "-i", "aevalsrc=exprs=0",
        
        "-vf", (
            # 1. Background Tint (Make it darker)
            "colorchannelmixer=rr=0.1:gg=0.1:bb=0.2,"
            
            # 2. Main Title
            "drawtext=text='CHANNEL PROMOTION STATION':fontcolor=00FF00:fontsize=65:x=(w-tw)/2:y=100:box=1:boxcolor=black@0.9:boxborderw=20,"
            
            # 3. Current User Box
            "drawtext=textfile='current.txt':reload=1:fontcolor=cyan:fontsize=80:x=(w-tw)/2:y=600:box=1:boxcolor=black@0.8:boxborderw=20:line_spacing=20:text_align=C,"
            
            # 4. Queue List
            "drawtext=textfile='queue.txt':reload=1:fontcolor=white:fontsize=50:x=100:y=1200:box=1:boxcolor=black@0.7:boxborderw=15:line_spacing=10,"
            
            # 5. Instructions at bottom
            "drawtext=text='SUBSCRIBE & TYPE IN CHAT TO GET PROMOTED!':fontcolor=yellow:fontsize=45:x=(w-tw)/2:y=1750:box=1:boxcolor=black@0.8:boxborderw=10"
        ),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "2500k",    # Higher Bitrate for 2K-like clarity
        "-maxrate", "2500k",
        "-bufsize", "5000k",
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
            print("[!] Stream Drop. Restarting Engine...")
            time.sleep(3)
        except:
            time.sleep(3)

if __name__ == "__main__":
    print("=== BEASTGPT SHORT-LIVE MATRIX ===")
    
    # Initialize text files
    open("current.txt", "w").close()
    open("queue.txt", "w").close()
    
    # Start processes
    threading.Thread(target=update_ui_files, daemon=True).start()
    threading.Thread(target=queue_manager, daemon=True).start()
    threading.Thread(target=chat_sniper, daemon=True).start()
    
    # Start Stream
    stream_engine()
