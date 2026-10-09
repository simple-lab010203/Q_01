#!/usr/bin/env bash
# 로고 버전(유튜브, index.html)과 핸들 버전(X, index_handle.html)을 함께 렌더한다.
set -e
cd "$(dirname "$0")/.."
sed -e 's/ending: "logo"/ending: "handle"/' -e 's|assets/sfx.wav|assets/sfx_handle.wav|' index.html > index_handle.html
npx hyperframes render -c ./index.html -o out/innovation_logo.mp4
npx hyperframes render -c ./index_handle.html -o out/innovation_handle.mp4
