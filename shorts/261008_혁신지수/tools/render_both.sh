#!/usr/bin/env bash
# 로고 버전(index.html)과 핸들 버전(index_handle.html)을 함께 렌더한다.
set -e
cd "$(dirname "$0")/.."
sed 's/ending: "logo"/ending: "handle"/' index.html > index_handle.html
npx hyperframes render -c ./index.html -o out/innovation_logo.mp4
npx hyperframes render -c ./index_handle.html -o out/innovation_handle.mp4
