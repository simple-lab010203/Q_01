# 한국 혁신 순위 10위 → 4위 (모션 쇼츠, 48초)

- 로고 버전(유튜브): `out/innovation_logo.mp4` — 구독 버튼 + 로고 + 핸들 + 출처
- 핸들 버전(X): `out/innovation_handle.mp4` — 핸들 + 출처 (구독 버튼·로고 없음)
- 1080x1920, 30fps
- 데이터: WIPO 글로벌 혁신지수 2020~2026 한국 순위 10·5·6·10·6·4·4 (원자료 대조 완료)
- 수치·데이터 영상이라 먼지 캐릭터 없이 차트와 글자로만 구성

## 키트 소재로 바꾸기 (같은 파일명으로 `assets/`에 넣고 다시 렌더)
- `KyoboHandwriting2025lyb.ttf` → 교보 손글씨 (라이선스상 저장소에 올리지 않음, 없으면 대체 폰트 Gaegu)
- `bgm.wav` → Circa 1983 - Freedom Trail Studio (0.76초부터 48초, -22 LUFS, 끝 1초 페이드아웃). 음원이라 저장소에 올리지 않음
- 효과음: `sfx.wav`(로고 버전), `sfx_handle.wav`(핸들 버전) — `python3 tools/make_audio.py`로 생성 (임시 합성 BGM도 같이 생성되니 실제 곡으로 다시 덮어쓸 것)

## 숫자 바꾸기
`index.html` 맨 위 `window.CFG`의 `korea` 배열만 고치면 차트가 바뀜 (캡션 문구는 `#cap0`~`#cap6`).

## 렌더
`tools/render_both.sh` → 두 버전을 함께 렌더 (`index.html`의 `CFG.ending`으로 구분)
