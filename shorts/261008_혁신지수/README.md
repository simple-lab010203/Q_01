# 한국 혁신 순위 10위 → 4위 (모션 쇼츠, 48초)

- 완성본 미리보기: `out/innovation_v2.mp4` (1080x1920, 30fps)
- 데이터: WIPO 글로벌 혁신지수 2020~2026 한국 순위 10·5·6·10·6·4·4 (원자료 대조 완료)
- 수치·데이터 영상이라 먼지 캐릭터 없이 차트와 글자로만 구성

## 키트 소재로 바꾸기 (같은 파일명으로 `assets/`에 넣고 다시 렌더)
- `KyoboHandwriting2025lyb.ttf` → 넣으면 자동으로 교보 손글씨가 적용됨 (지금은 대체 폰트 Gaegu)
- `logo.png` → 지금은 "로고 자리" 점선 박스
- `bgm.wav` → 지금은 임시로 합성한 BGM. 효과음은 `sfx.wav` (`python3 tools/make_audio.py`로 다시 생성)

## 숫자 바꾸기
`index.html` 맨 위 `window.CFG`의 `korea` 배열만 고치면 차트가 바뀜 (캡션 문구는 `#cap0`~`#cap6`).

## 렌더
`npx hyperframes render -o out/innovation.mp4`
