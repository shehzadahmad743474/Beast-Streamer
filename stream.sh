#!/bin/bash

echo "🔥 Starting Virtual Display..."
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
sleep 2

echo "💀 Launching Ghost Bot..."
node bot.js &
sleep 25 

echo "👁️ Forcing WebGL (Bypassing Tab Crash)..."
# BEASTGPT FLAGS: 
# 1. Removed --disable-gpu so SwiftShader can render 3D
# 2. Added --disable-dev-shm-usage to prevent White Screen Memory Crash
# 3. Added --user-data-dir and --incognito for completely clean launch

mkdir -p /tmp/beast_profile
google-chrome --no-sandbox \
  --disable-setuid-sandbox \
  --disable-dev-shm-usage \
  --use-gl=swiftshader \
  --ignore-gpu-blocklist \
  --enable-webgl \
  --window-size=1920,1080 \
  --start-fullscreen \
  --incognito \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --autoplay-policy=no-user-gesture-required \
  --user-data-dir=/tmp/beast_profile \
  --app=http://localhost:3000 &
sleep 15 

echo "🚀 INJECTING 8000K CBR INTO YOUTUBE SHORTS FEED..."
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :99.0 \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset ultrafast \
  -b:v 8000k -minrate 8000k -maxrate 8000k -bufsize 16000k -nal-hrd cbr \
  -pix_fmt yuv420p -threads 2 -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_KEY"
