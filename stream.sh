#!/bin/bash

echo "🎵 Downloading No-Copyright LoFi Music..."
# Download royalty-free track automatically
wget -q -O bgm.mp3 "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"

echo "🔥 Starting Virtual Display with GLX..."
# +extension GLX zaroori hai WebGL software render ke liye
Xvfb :99 -screen 0 1920x1080x24 +extension GLX &
export DISPLAY=:99
sleep 3

echo "💀 Launching Ghost Bot..."
node bot.js &
sleep 20 # Waiting for chunks to load

echo "👁️ Forcing Absolute Headless Eye..."
mkdir -p /tmp/beast_profile
# No-GPU flags strictly enforced for GitHub Actions
google-chrome --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --use-gl=swiftshader \
  --enable-webgl \
  --ignore-gpu-blocklist \
  --window-size=1920,1080 \
  --start-fullscreen \
  --incognito \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --user-data-dir=/tmp/beast_profile \
  --app=http://localhost:3000 > /dev/null 2>&1 &
sleep 15 

echo "🚀 INJECTING AUDIO+VIDEO INTO YOUTUBE SHORTS FEED..."
# -stream_loop -1 : Music ko hamesha repeat karega
# 4000k bitrate is perfectly stable for 1080x1920 Shorts Feed
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :99.0 \
  -stream_loop -1 -i bgm.mp3 \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset veryfast -b:v 4000k -maxrate 4000k -bufsize 8000k -pix_fmt yuv420p -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_KEY"
