import os
import time
import subprocess
import threading
import logging
import requests
import re

# Silence errors
logging.getLogger("pytchat").setLevel(logging.CRITICAL)
import pytchat

# --- SECRETS FETCHED FROM GITHUB ---
STREAM_KEY = os.environ.get('STREAM_KEY')
YOUTUBE_RTMP = "rtmp://a.rtmp.youtube.com/live2/"
LIVE_VIDEO_ID = os.environ.get('VIDEO_ID')

DEFAULT_VIDEO = "default.mp4"
if not os.path.exists(DEFAULT_VIDEO):
    os.system('wget -q -O default.mp4 "https://www.w3schools.com/html/mov_bbb.mp4"')

target_queue = []
stream_process = None

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
        countdown_filter = f"drawtext=text='TIME LEFT\: %{{eif\:{duration}-t\:d}}S':fontcolor=yellow:fontsize=80:x=(w-text_w)/2:y=150:box=1:boxcolor=red@0.8:boxborderw=15,"
        time_limit = ["-t", str(duration)]

    filter_chain = (
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"{countdown_filter}"
        f"drawtext=text='TARGET\: {safe_user}':fontcolor=cyan:fontsize=70:x=40:y=60:box=1:boxcolor=black@0.7:boxborderw=10,"
        f"drawtext=text='TITLE\: {safe_title}':fontcolor=lime:fontsize=60:x=40:y=h-180:box=1:boxcolor=black@0.7:boxborderw=15"
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
    print("💀 Master Encoder Online. GitHub Server is LIVE.")
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
                play_video(DEFAULT_VIDEO, "NO TARGET", "SEND A MESSAGE IN CHAT", duration=0)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if not STREAM_KEY or not LIVE_VIDEO_ID:
        print("ERROR: Stream Key or Video ID missing from GitHub Secrets!")
        exit()
    threading.Thread(target=chat_sniper, daemon=True).start()
    stream_engine()
