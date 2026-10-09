#!/usr/bin/env bash
# 로고 버전(유튜브, index.html)과 핸들 버전(X, index_handle.html)을 함께 렌더하고
# 최종 음량을 쇼츠 기준(-14 LUFS)으로 맞춘다.
set -e
cd "$(dirname "$0")/.."
sed -e 's/ending: "logo"/ending: "handle"/' -e 's|assets/sfx.wav|assets/sfx_handle.wav|' index.html > index_handle.html
for v in logo handle; do
  src=index.html; [ "$v" = handle ] && src=index_handle.html
  npx hyperframes render -c "./$src" -o "out/raw_$v.mp4"
  ffmpeg -loglevel error -y -i "out/raw_$v.mp4" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
    -c:a aac -b:a 192k -ar 48000 "out/innovation_$v.mp4"
  rm "out/raw_$v.mp4"
done
