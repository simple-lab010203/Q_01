"""효과음 트랙(sfx.wav)과 임시 배경음악(bgm.wav)을 합성한다.
키트 bgm을 쓸 때는 assets/bgm.wav 만 교체하면 된다.
실행: python3 tools/make_audio.py
"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 48.0
OUT = Path(__file__).resolve().parent.parent / "assets"
rng = np.random.default_rng(3)


def env(n, attack=0.004, decay=0.08):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def tick():
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    return 0.5 * np.sin(2 * np.pi * 2200 * t) * env(n, 0.001, 0.012)


def click():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 3400 * t) * env(n, 0.0005, 0.006)
    s += 0.6 * np.sin(2 * np.pi * 900 * t) * env(n, 0.0005, 0.015)
    return 0.7 * s


def boop():
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    f = 500 + 1300 * (t / t[-1]) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.35 * np.sin(ph) * env(n, 0.003, 0.07)


def swish():
    n = int(0.32 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # 간단한 1차 저역통과 필터를 시간에 따라 열었다 닫음
    cut = 0.05 + 0.35 * np.sin(np.pi * t / t[-1])
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc += cut[i] * (noise[i] - acc)
        y[i] = acc
    shape = np.sin(np.pi * t / t[-1]) ** 2
    return 0.45 * y * shape / (np.abs(y).max() + 1e-9)


def pang():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (140 * np.exp(-t * 18) + 60) * t) * env(n, 0.002, 0.12)
    burst = rng.standard_normal(n) * env(n, 0.001, 0.05)
    sparkle = sum(np.sin(2 * np.pi * f * t) for f in (1568, 2093, 2637)) / 3 * env(n, 0.002, 0.18)
    return 0.6 * body + 0.25 * burst + 0.25 * sparkle


def thud():
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    f = 220 * np.exp(-t * 6) + 70
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.6 * np.sin(ph) * env(n, 0.002, 0.14)


EVENTS = [
    # 1. 훅
    (0.2, boop), (0.8, tick), (1.4, boop), (1.8, pang), (2.4, swish), (3.0, tick),
    # 장면 전환
    (4.6, boop), (9.4, boop), (29.4, boop), (35.4, boop), (41.4, boop),
    # 2. 설명
    (5.3, tick), (6.0, swish), (6.6, tick), (7.0, tick), (7.8, tick),
    # 3. 차트: 단계별 하이라이트(슥)와 도착(틱)
    (10.0, swish), (10.9, tick),
    (12.35, swish), (12.9, tick),
    (15.05, swish), (15.6, tick),
    (17.35, swish), (17.9, thud),
    (20.35, swish), (20.9, tick),
    (22.75, swish), (23.3, pang),
    (26.15, swish), (26.7, tick),
    # 4. 순위 리스트
    (30.5, tick), (31.05, tick), (31.6, tick), (32.4, pang), (33.0, swish),
    # 5. 강점
    (36.1, tick), (37.2, swish), (38.4, tick),
    # 6. 마무리
    (42.2, swish), (43.4, boop), (44.6, click), (45.2, tick),
]


def make_sfx():
    out = np.zeros(int(DUR * SR))
    for t0, fn in EVENTS:
        s = fn()
        i = int(t0 * SR)
        out[i : i + len(s)] += s[: len(out) - i]
    return out


def make_bgm():
    """96 BPM의 가벼운 플럭 루프 (C - Am - F - G)."""
    out = np.zeros(int(DUR * SR))
    beat = 60 / 96
    chords = [
        [60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62],
    ]
    mel = [72, 76, 79, 76, 74, 76, 72, 69]

    def note(midi, length, vol, decay):
        n = int(length * SR)
        t = np.arange(n) / SR
        f = 440 * 2 ** ((midi - 69) / 12)
        s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
        return vol * s * env(n, 0.006, decay)

    t = 0.0
    k = 0
    while t < DUR:
        bar = int(t / (beat * 4)) % 4
        ch = chords[bar]
        i = int(t * SR)

        def put(s):
            out[i : i + len(s)] += s[: max(0, len(out) - i)]

        put(note(ch[0] - 12, beat * 1.8, 0.22, 0.35))  # 베이스
        if k % 2 == 1:
            for m in ch:
                put(note(m, beat, 0.05, 0.18))  # 오프비트 코드
        if k % 2 == 0:
            put(note(mel[(k // 2) % len(mel)], beat, 0.07, 0.22))
        hat = rng.standard_normal(int(0.03 * SR)) * env(int(0.03 * SR), 0.001, 0.008) * 0.04
        put(hat)
        t += beat
        k += 1
    fade = int(1.0 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def save(name, x, peak):
    x = x / (np.abs(x).max() + 1e-9) * peak
    data = (x * 32767).astype(np.int16)
    with wave.open(str(OUT / name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


if __name__ == "__main__":
    save("sfx.wav", make_sfx(), 0.9)
    save("bgm.wav", make_bgm(), 0.35)  # 효과음보다 작게
    print("ok")
