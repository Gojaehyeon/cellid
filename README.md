# Cellid

맥북 힌지를 활처럼 켜는 첼로. 키보드는 Logic Pro Musical Typing 매핑(왼손=음정), 힌지 각속도가 활(오른손=음량/표현력)이다.

## 작동

- 키보드로 음정을 누른다 — `A S D F G H J K L ;` (흰건반), `W E T Y U O P` (검은건반)
- 화면 뚜껑(lid)을 위아래로 움직이면 활을 켜는 것과 같다
- 멈추면 음이 빠르게 사라진다 (실제 첼로처럼 활이 멈추면 무음)
- lid 절대 각도는 음색을 좌우한다 — 닫혀 있을수록 mute, 열릴수록 brilliant

## 키맵

| 키 | 음 |
|---|---|
| Z / X | 옥타브 ↓ / ↑ |
| Tab (hold) | sustain 페달 |
| A W S E D F T G Y H U J | C C# D D# E F F# G G# A A# B |
| K O L P ; | C C# D D# E (한 옥타브 위) |

## 실행

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

그리고 브라우저로 [http://localhost:8088](http://localhost:8088) 열기. lid 데이터는 `ws://localhost:8765` 로 푸시된다.

## 의존성

- `pybooklid` — Apple 실리콘 맥북의 lid 각도 센서 (HID)
- `websockets` — 브라우저 ↔ 센서 브릿지
- `hidapi` — pybooklid 백엔드
