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
current_target = "NO ONE. SEND A MESSAGE!"

def update_ui_files():
    """Ye function har second text files update karega jise FFmpeg live screen par kheechega"""
    while True:
        try:
            # Current User File
            with open("current.txt", "w", encoding="utf-8") as f:
                f.write(f"👉 NOW SHOWING 👈\n\n {current_target.upper()} ")
            
            # Queue File
            q_text = "⏳ WAITING LIST:\n\n"
            if len(user_queue) == 0:
                q_text += "Empty. Type in chat to join!"
            else:
                for i, u in enumerate(user_queue[:5]): # Top 5 log screen par dikhenge
                    q_text += f"{i+1}. {u}\n"
            
            with open("queue.txt", "w", encoding="utf-8") as f:
                f.write(q_text)
                
            time.sleep(1)
        except:
            pass

def queue_manager():
    """Ye queue chalayega, har user ko screen par 30 seconds dega"""
    global current_target, user_queue
    while True:
        if len(user_queue) > 0:
            current_target = user_queue.pop(0)
            print(f"[*] Spotlight on: {current_target}")
            time.sleep(30) # 30 Second tak screen par rahega
        else:
            current_target = "SEND ANY MESSAGE TO JOIN!"
            time.sleep(5)

def chat_sniper():
    """Ye chat padhega aur nayi entries ko line mein lagayega"""
    global user_queue
    print("💀 Chat Sniper Active. Monitoring Live Chat...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    author = c.author.name
                    print(f"💬 Chat from {author}: {c.message}")
                    
                    # Agar user line mein nahi hai, toh add karo
                    if author not in user_queue and author != current_target:
                        user_queue.append(author)
                        print(f"[+] Added {author} to Queue. Queue size: {len(user_queue)}")
        except Exception as e:
            print(f"[-] Chat Disconnected. Retrying... {e}")
            time.sleep(10)

def stream_engine():
    """BeastGPT Dynamic Video Generator"""
    print("💀 Master Encoder Online. Generating Dynamic UI...")
    
    # 1. Hum FFmpeg se ek Virtual Black Video create kar rahe hain (color=c=black)
    # 2. Virtual Silent Audio (aevalsrc=exprs=0)
    # 3. drawtext filter un text files ko padhkar real-time video par chipkayega!
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-f", "lavfi", "-i", "color=c=black:s=1280x720:r=30",  # Fake background
        "-f", "lavfi", "-i", "aevalsrc=exprs=0",               # Fake audio
        "-vf", (
            "drawtext=text='🔥 LIVE CHANNEL PROMOTION & QUEUE 🔥':fontcolor=lime:fontsize=45:x=(w-tw)/2:y=50:box=1:boxcolor=black@0.8:boxborderw=10,"
            "drawtext=textfile='current.txt':reload=1:fontcolor=yellow:fontsize=60:x=(w-tw)/2:y=250:box=1:boxcolor=red@0.5:boxborderw=15,"
            "drawtext=textfile='queue.txt':reload=1:fontcolor=white:fontsize=35:x=50:y=450:box=1:boxcolor=blue@0.4:boxborderw=10"
        ),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "1500k",
        "-maxrate", "1500k",
        "-bufsize", "3000k",
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
    print("=== BEASTGPT INTERACTIVE MATRIX ===")
    # Create files so FFmpeg doesn't crash on start
    open("current.txt", "w").close()
    open("queue.txt", "w").close()
    
    # Start all threads
    threading.Thread(target=update_ui_files, daemon=True).start()
    threading.Thread(target=queue_manager, daemon=True).start()
    threading.Thread(target=chat_sniper, daemon=True).start()
    
    # Run Stream
    stream_engine()
