#!/bin/bash

echo "🔥 Starting Virtual Display..."
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
sleep 2

echo "💀 Launching Ghost Bot..."
node bot.js &
# Bot ko duniya render karne aur chunks load karne ka poora time do
sleep 25 

echo "👁️ Forcing WebGL through CPU (Bypassing White Screen)..."
# BEASTGPT FLAGS: Force WebGL rendering even without a GPU
google-chrome --no-sandbox \
  --disable-gpu \
  --use-gl=swiftshader \
  --ignore-gpu-blocklist \
  --enable-webgl \
  --window-size=1920,1080 \
  --start-fullscreen \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --app=http://localhost:3000 &
sleep 15 # Chrome ko 3D load karne ka time do

echo "🚀 INJECTING 8000K CBR INTO YOUTUBE SHORTS FEED..."
# BEASTGPT 8000K LOCK: -minrate aur -maxrate dono 8000k par set, -nal-hrd cbr forces strict bitrate
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :99.0 \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset ultrafast \
  -b:v 8000k -minrate 8000k -maxrate 8000k -bufsize 16000k -nal-hrd cbr \
  -pix_fmt yuv420p -threads 2 -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_KEY"
