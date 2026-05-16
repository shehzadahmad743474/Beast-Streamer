#!/bin/bash

echo "🔥 Starting Virtual Display..."
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
sleep 2

echo "💀 Launching Ghost Bot..."
node bot.js &
sleep 15 # Wait for bot

echo "👁️ Opening Headless Eye (Silent Chrome)..."
# BEASTGPT FLAGS: Disable all popups, welcome screens, and crash reports
google-chrome --no-sandbox \
  --disable-gpu \
  --use-gl=swiftshader \
  --window-size=1920,1080 \
  --start-fullscreen \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --app=http://localhost:3000 &
sleep 10

echo "🚀 INJECTING INTO YOUTUBE SHORTS FEED (9:16 CROP)..."
ffmpeg -f x11grab -video_size 1920x1080 -framerate 20 -i :99.0 \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset ultrafast -b:v 1500k -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -threads 2 -g 40 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_KEY"
