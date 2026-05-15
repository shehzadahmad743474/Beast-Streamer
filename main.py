import os
import time
import subprocess
import threading
import logging
import requests
import re
import urllib.request
import json

# Silence errors
logging.getLogger("pytchat").setLevel(logging.CRITICAL)
import pytchat

# --- SECRETS FETCHED FROM GITHUB ---
STREAM_KEY = os.environ.get('STREAM_KEY')
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
LIVE_VIDEO_ID = os.environ.get('VIDEO_ID')

# 🔴 BEASTGPT HARDCODED API KEY (Rules are meant to be broken) 🔴
API_KEY = "AIzaSyAfDtjWNC1O29ER5tIfFcHo3GK81jw5aZs"

DEFAULT_VIDEO = "default.mp4"
STATS_FILE = "real_stats.txt"

if not os.path.exists(DEFAULT_VIDEO):
    os.system('wget -q -O default.mp4 "https://www.w3schools.com/html/mov_bbb.mp4"')

with open(STATS_FILE, "w", encoding="utf-8") as f:
    f.write("🔥 CONNECTING TO YOUTUBE SERVER FOR REAL STATS... 🔥")

target_queue = []
stream_process = None

# --- REAL STATS ENGINE (YOUTUBE API) ---
def real_stats_engine():
    print("💀 Real Stats Engine ACTIVE. Tapping into YouTube API...")
    # Spoofing headers so Google doesn't block the Python/urllib request easily
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    while True:
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails,statistics&id={LIVE_VIDEO_ID}&key={API_KEY}"
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                items = data.get('items', [])
                if items:
                    item = items[0]
                    # Agar stream live nahi hui (scheduled hai), toh ye data exist nahi karta
                    if 'liveStreamingDetails' in item:
                        viewers = item['liveStreamingDetails'].get('concurrentViewers', '0')
                    else:
                        viewers = "0 (Scheduled)"
                        
                    likes = item.get('statistics', {}).get('likeCount', '0')
                    text = f"🔥 REAL LIVE STATS: {viewers} WATCHING | {likes} LIKES | DROP A MESSAGE TO PLAY YOUR VIDEO! 🔥"
                else:
                    text = "🔥 REAL LIVE STATS: WRONG VIDEO ID OR NOT LIVE YET 🔥"
            
            # Write to file for FFmpeg to read dynamically
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                f.write(text)
                
        except urllib.error.HTTPError as e:
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                f.write(f"🔥 API ERROR: {e.code} (CHECK KEY LIMITS) 🔥")
        except Exception as e:
            pass # Silent fail on network error, keep old text
            
        time.sleep(20) # Ping Google every 20 seconds

# --- DARK NODE EXTRACTOR ---
def get_user_video(channel_id):
    dark_nodes = [
        "https://invidious.nerdvpn.de", "https://inv.tux.pizza",
        "https://invidious.jing.rocks", "https://invidious.lunar.icu"
    ]
    for node in dark_nodes:
        try:
            print(f"[*] Probing Dark Node: {node}...")
            ch_url = f"{node}/api/v1/channels/{channel_id}"
            ch_res = requests.get(ch_url, timeout=5).json()
            
            if 'latestVideos' in ch_res and len(ch_res['latestVideos']) > 0:
                latest_vid_id = ch_res['latestVideos'][0]['videoId']
                title = ch_res['latestVideos'][0]['title']
                
                vid_url = f"{node}/api/v1/videos/{latest_vid_id}"
                vid_res = requests.get(vid_url, timeout=5).json()
                
                for stream in vid_res.get('formatStreams', []):
                    if 'mp4' in stream.get('type', '') and '720p' in stream.get('qualityLabel', ''):
                        return stream['url'], title
                for stream in vid_res.get('formatStreams', []):
                    if 'mp4' in stream.get('type', ''):
                        return stream['url'], title
        except Exception:
            continue
    return None, None

# --- CHAT SNIPER ---
def chat_sniper():
    global target_queue
    print("💀 Chat Sniper ACTIVE on GitHub Servers...")
    while True:
        try:
            chat = pytchat.create(video_id=LIVE_VIDEO_ID, interruptable=False)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    user_name = c.author.name
                    channel_id = c.author.channelId
                    if not any(u['id'] == channel_id for u in target_queue):
                        print(f"🔥 Target Added to Queue: {user_name}")
                        target_queue.append({'name': user_name, 'id': channel_id})
        except Exception:
            time.sleep(5)

# --- MASTER ENCODER ---
def clean_text(text):
    return re.sub(r'[^A-Za-z0-9 ]+', '', text)[:35]

def play_video(media_url, user_name, title, duration):
    global stream_process, target_queue
    safe_title, safe_user = clean_text(title), clean_text(user_name)
    countdown_filter, time_limit = "", []
    
    if duration > 0:
        countdown_filter = fr"drawtext=text='TIME LEFT\\: %{{eif\\:{duration}-t\\:d}}S':fontcolor=yellow:fontsize=80:x=(w-text_w)/2:y=150:box=1:boxcolor=red@0.8:boxborderw=15,"
        time_limit = ["-t", str(duration)]

    # 🔴 BEASTGPT REAL-TIME ANIMATED OVERLAY 🔴
    scrolling_stats = fr"drawtext=textfile='{STATS_FILE}':reload=1:fontcolor=yellow:fontsize=50:y=h-100:x=w-mod(t*250\,w+2500):box=1:boxcolor=black@0.6:boxborderw=10"

    filter_chain = (
        r"scale=1080:1920:force_original_aspect_ratio=decrease,"
        r"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
        + countdown_filter +
        fr"drawtext=text='REQUESTED BY\\: {safe_user}':fontcolor=cyan:fontsize=70:x=40:y=60:box=1:boxcolor=black@0.7:boxborderw=10,"
        fr"drawtext=text='NOW PLAYING\\: {safe_title}':fontcolor=lime:fontsize=60:x=40:y=h-250:box=1:boxcolor=black@0.7:boxborderw=15,"
        + scrolling_stats
    )

    ffmpeg_cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-re"]
    if duration == 0: ffmpeg_cmd.extend(["-stream_loop", "-1"])
    ffmpeg_cmd.extend(["-fflags", "+genpts", "-i", media_url])
    ffmpeg_cmd.extend(time_limit) 
    
    ffmpeg_cmd.extend([
        "-vf", filter_chain,
        "-c:v", "libx264", "-preset", "ultrafast", 
        "-b:v", "3000k", "-maxrate", "3000k", "-bufsize", "6000k", 
        "-pix_fmt", "yuv420p", "-g", "60",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-f", "flv", f"{YOUTUBE_RTMP}{STREAM_KEY}"
    ])
    
    stream_process = subprocess.Popen(ffmpeg_cmd)
    
    if duration == 0:
        while stream_process.poll() is None:
            if len(target_queue) > 0:
                print("\n[!] New Target! Killing Default Stream...")
                stream_process.terminate()
                stream_process.wait()
                break
            time.sleep(2)
    else:
        stream_process.wait()

def stream_engine():
    global target_queue
    print("💀 Master Encoder Online. GitHub Server is LIVE with REAL STATS.")
    while True:
        try:
            if len(target_queue) > 0:
                target = target_queue.pop(0)
                raw_url, title = get_user_video(target['id'])
                if raw_url:
                    play_video(raw_url, target['name'], title, duration=60)
                else:
                    time.sleep(2)
            else:
                play_video(DEFAULT_VIDEO, "NO USER YET", "SEND A MESSAGE IN CHAT", duration=0)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if not STREAM_KEY or not LIVE_VIDEO_ID:
        print("ERROR: Stream Key or Video ID missing from GitHub Secrets!")
        exit()
    
    threading.Thread(target=real_stats_engine, daemon=True).start()
    threading.Thread(target=chat_sniper, daemon=True).start()
    stream_engine()
