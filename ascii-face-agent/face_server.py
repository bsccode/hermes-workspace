#!/usr/bin/env python3
import argparse
import json
import random
import selectors
import signal
import socket
import sys
import textwrap
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

EMOTIONS = {
    "neutral": {"brows": (" ", " "), "eyes_open": ("o", "o"), "eyes_closed": ("-", "-"), "mouth": ["___", "___", "_~_", "---"]},
    "happy": {"brows": ("^", "^"), "eyes_open": ("^", "^"), "eyes_closed": ("-", "-"), "mouth": ["\\___/", "\\_U_/", "\\___/"]},
    "sad": {"brows": ("'", "'"), "eyes_open": ("u", "u"), "eyes_closed": ("-", "-"), "mouth": ["/___\\", "/_-_\\"]},
    "angry": {"brows": ("/", "\\"), "eyes_open": (">", "<"), "eyes_closed": ("-", "-"), "mouth": ["__^__", "_===_", "_> <_"]},
    "surprised": {"brows": ("o", "o"), "eyes_open": ("O", "O"), "eyes_closed": ("-", "-"), "mouth": [" (O) ", " (o) "]},
    "thinking": {"brows": ("~", "_"), "eyes_open": ("-", "o"), "eyes_closed": ("-", "-"), "mouth": [" _/ ", " __? ", " _.. "]},
    "sleepy": {"brows": ("_", "_"), "eyes_open": ("-", "-"), "eyes_closed": ("-", "-"), "mouth": [" zzz ", " ___ "]},
    "excited": {"brows": ("*", "*"), "eyes_open": ("*", "*"), "eyes_closed": ("x", "x"), "mouth": ["\\___/", "\\_O_/", "\\___/"]},
}

TALK_FRAMES = [" (o) ", " (O) ", " \\_/ ", " \\o/ ", " _o_ "]
STREAM_CURSOR = "▋"
STATUS_DURATION = 4.0
STREAM_CLEAR_DELAY = 1.25
BEEP_INTERVAL_TICKS = 4
DEFAULT_SOCKET = "/tmp/ascii-face-agent.sock"


POSITIVE_CUES = ("!", "yay", "great", "awesome", "nice", "love", "solved", "done", "yes", "perfect", "complete", "working!")
THINKING_CUES = ("hmm", "thinking", "let me", "consider", "maybe", "analy", "reason", "check", "work through", "working on")
SAD_CUES = ("sorry", "failed", "can't", "cannot", "won't", "unable", "error", "issue", "problem", "missed")
ANGRY_CUES = ("danger", "warning", "critical", "stop", "alert", "bad", "broken", "risk")
SURPRISED_CUES = ("?", "whoa", "wow", "what", "really", "unexpected")
SLEEPY_CUES = ("zzz", "sleepy", "tired", "exhausted")


@dataclass
class FaceState:
    emotion: str = "neutral"
    text: str = "waiting for a mind"
    look_x: int = 0
    blink_until: float = 0.0
    speaking_until: float = 0.0
    mouth_override: Optional[str] = None
    status_until: float = 0.0
    pulse_until: float = 0.0
    shutdown: bool = False
    streaming: bool = False
    auto_emote: bool = True
    beep_enabled: bool = True
    fps: int = 12
    lock: threading.RLock = field(default_factory=threading.RLock)

    def snapshot(self) -> dict[str, Any]:
        now = time.time()
        with self.lock:
            visible_text = self.text if self.streaming or now < self.status_until else ""
            return {
                "emotion": self.emotion,
                "text": visible_text,
                "look_x": self.look_x,
                "blink": now < self.blink_until,
                "speaking": now < self.speaking_until,
                "mouth_override": self.mouth_override,
                "pulse": now < self.pulse_until,
                "shutdown": self.shutdown,
                "streaming": self.streaming,
                "auto_emote": self.auto_emote,
                "beep_enabled": self.beep_enabled,
            }

    def _refresh_speaking(self, now: float, text: str, payload: dict[str, Any]) -> None:
        duration = float(payload.get("duration", max(0.45, min(len(text) * 0.05, 8.0))))
        self.speaking_until = max(self.speaking_until, now + duration)

    def _apply_emotion_from_text(self, text: str, payload: dict[str, Any], now: float) -> None:
        if payload.get("emotion"):
            return
        auto_emote = payload.get("auto_emote")
        if auto_emote is not None:
            self.auto_emote = bool(auto_emote)
        if not self.auto_emote:
            return
        inferred = infer_emotion_from_text(text)
        self.emotion = inferred
        if inferred in {"excited", "surprised", "angry"}:
            self.pulse_until = max(self.pulse_until, now + 0.45)

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = time.time()
        with self.lock:
            if payload.get("reset"):
                self.emotion = "neutral"
                self.text = "waiting for a mind"
                self.look_x = 0
                self.blink_until = 0.0
                self.speaking_until = 0.0
                self.mouth_override = None
                self.status_until = now + STATUS_DURATION
                self.pulse_until = 0.0
                self.streaming = False
                self.auto_emote = True
                self.beep_enabled = True

            emotion = payload.get("emotion")
            if emotion:
                if emotion not in EMOTIONS:
                    raise ValueError(f"Unknown emotion: {emotion}")
                self.emotion = emotion

            if "look" in payload:
                look = payload["look"]
                if isinstance(look, (list, tuple)) and look:
                    look_x = int(look[0])
                else:
                    look_x = int(look)
                self.look_x = max(-1, min(1, look_x))

            if payload.get("blink"):
                self.blink_until = now + float(payload.get("blink_duration", 0.18))

            if payload.get("pulse"):
                self.pulse_until = now + float(payload.get("pulse_duration", 0.7))

            if "mouth" in payload:
                self.mouth_override = str(payload["mouth"]) if payload["mouth"] else None

            if "beep" in payload:
                self.beep_enabled = bool(payload["beep"])

            if payload.get("stream_start"):
                self.streaming = True
                if payload.get("clear", True):
                    self.text = ""
                self.status_until = now + 3600

            if "stream_chunk" in payload:
                self.streaming = True
                chunk = str(payload.get("stream_chunk") or "")
                self.text += chunk
                self.status_until = now + 3600
                self._refresh_speaking(now, chunk or self.text, payload)
                self._apply_emotion_from_text(self.text, payload, now)

            spoken = payload.get("say") or payload.get("speak")
            if spoken is not None:
                self.streaming = False
                self.text = str(spoken)
                self.status_until = now + float(payload.get("text_duration", STATUS_DURATION))
                self._refresh_speaking(now, self.text, payload)
                self._apply_emotion_from_text(self.text, payload, now)

            if "text" in payload:
                self.text = str(payload["text"])
                self.status_until = now + (3600 if self.streaming else float(payload.get("text_duration", STATUS_DURATION)))
                if payload.get("stream_start") or self.streaming:
                    self._apply_emotion_from_text(self.text, payload, now)

            if payload.get("stream_end"):
                self.streaming = False
                clear_after = float(payload.get("clear_after", payload.get("text_duration", STREAM_CLEAR_DELAY)))
                self.status_until = now + max(0.0, clear_after)
                self._refresh_speaking(now, self.text, payload)
                self._apply_emotion_from_text(self.text, payload, now)

            if payload.get("shutdown"):
                self.shutdown = True

            return self.snapshot()


def infer_emotion_from_text(text: str) -> str:
    lowered = (text or "").strip().lower()
    if not lowered:
        return "neutral"

    tail = lowered[-80:]
    normalized_tail = tail.replace("?", ".").replace("!", ".")
    last_clause = normalized_tail.split(".")[-1].strip() or tail

    if any(cue in last_clause for cue in POSITIVE_CUES) or any(cue in tail for cue in POSITIVE_CUES):
        return "excited"
    if any(cue in last_clause for cue in SURPRISED_CUES) or any(cue in tail for cue in SURPRISED_CUES):
        return "surprised"
    if any(cue in last_clause for cue in SLEEPY_CUES) or any(cue in tail for cue in SLEEPY_CUES):
        return "sleepy"
    if any(cue in lowered for cue in ANGRY_CUES):
        return "angry"
    if any(cue in lowered for cue in SAD_CUES):
        return "sad"
    if any(cue in lowered for cue in THINKING_CUES):
        return "thinking"
    if any(cue in lowered for cue in SURPRISED_CUES):
        return "surprised"
    if any(cue in lowered for cue in POSITIVE_CUES):
        return "excited"
    return "neutral"


def should_emit_beep(snapshot: dict[str, Any], tick: int, last_beep_tick: int, interval_ticks: int = BEEP_INTERVAL_TICKS) -> bool:
    if not snapshot.get("beep_enabled", True):
        return False
    if not (snapshot.get("streaming") or (snapshot.get("speaking") and snapshot.get("text"))):
        return False
    return tick - last_beep_tick >= interval_ticks


def render_face(snapshot: dict[str, Any], tick: int) -> str:
    spec = EMOTIONS[snapshot["emotion"]]
    closed = snapshot["blink"]
    eyes = list(spec["eyes_closed"] if closed else spec["eyes_open"])
    brows = list(spec["brows"])
    look_x = snapshot["look_x"]

    if snapshot["speaking"] and look_x == 0:
        look_x = [-1, 0, 1, 0][tick % 4]

    if not closed:
        if look_x < 0:
            eyes[0] = eyes[0].lower() if eyes[0].isalpha() else eyes[0]
            eyes[1] = "."
        elif look_x > 0:
            eyes[0] = "."
            eyes[1] = eyes[1].lower() if eyes[1].isalpha() else eyes[1]

    if snapshot["mouth_override"]:
        mouth = snapshot["mouth_override"]
    elif snapshot["speaking"]:
        mouth = TALK_FRAMES[tick % len(TALK_FRAMES)]
    else:
        mouth = spec["mouth"][tick % len(spec["mouth"])]

    forehead = "  " + brows[0] + "     " + brows[1] + "  "
    eyes_line = f" |   {eyes[0]}   {eyes[1]}   |"
    nose_line = " |     ^     |"
    mouth_line = f" |  {mouth.center(7)}  |"
    shell_left = "/" if snapshot["pulse"] and tick % 2 == 0 else "."
    shell_right = "\\" if snapshot["pulse"] and tick % 2 == 0 else "."
    lines = [
        "",
        f"    {forehead}",
        f"   {shell_left}-----------{shell_right}",
        eyes_line,
        nose_line,
        mouth_line,
        "   '-----------'",
        "",
    ]

    text = snapshot["text"].strip()
    if text:
        if snapshot.get("streaming"):
            text += STREAM_CURSOR if tick % 2 == 0 else " "
        wrapped = textwrap.wrap(text, width=48)[:3]
        for line in wrapped:
            lines.append(f"   {line}")
    else:
        lines.append("   ")

    mode = "streaming" if snapshot.get("streaming") else "idle"
    lines.append(f"   mode: {mode} | commands: emotion, say, blink, look, pulse, reset, shutdown, stream_*")
    return "\n".join(lines)


class FaceServer(threading.Thread):
    def __init__(self, socket_path: str, state: FaceState):
        super().__init__(daemon=True)
        self.socket_path = socket_path
        self.state = state
        self.selector = selectors.DefaultSelector()
        self.sock: Optional[socket.socket] = None

    def run(self) -> None:
        path = Path(self.socket_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.socket_path)
        self.sock.listen()
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ)

        while not self.state.snapshot()["shutdown"]:
            for key, _ in self.selector.select(timeout=0.2):
                if key.fileobj is self.sock:
                    conn, _ = self.sock.accept()
                    conn.setblocking(True)
                    self.handle_client(conn)

        self.cleanup()

    def handle_client(self, conn: socket.socket) -> None:
        with conn:
            file = conn.makefile("rwb")
            for raw in file:
                line = raw.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                    response = {"ok": True, "state": self.state.apply(payload)}
                except Exception as exc:
                    response = {"ok": False, "error": str(exc)}
                file.write((json.dumps(response) + "\n").encode("utf-8"))
                file.flush()
                if self.state.snapshot()["shutdown"]:
                    break

    def cleanup(self) -> None:
        try:
            if self.sock is not None:
                self.selector.unregister(self.sock)
                self.sock.close()
        except Exception:
            pass
        try:
            Path(self.socket_path).unlink(missing_ok=True)
        except Exception:
            pass


class TerminalFace:
    def __init__(self, state: FaceState, socket_path: str):
        self.state = state
        self.socket_path = socket_path
        self.tick = 0
        self.last_beep_tick = -BEEP_INTERVAL_TICKS
        now = time.time()
        self.next_blink_at = now + random.uniform(2.5, 5.5)

    def draw(self) -> None:
        sys.stdout.write("\x1b[?25l")
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()
        try:
            while not self.state.snapshot()["shutdown"]:
                now = time.time()
                if now >= self.next_blink_at:
                    self.state.apply({"blink": True})
                    self.next_blink_at = now + random.uniform(2.5, 5.5)
                snapshot = self.state.snapshot()
                frame = render_face(snapshot, self.tick)
                sys.stdout.write("\x1b[H")
                sys.stdout.write(frame)
                sys.stdout.write(f"\n\n   socket: {self.socket_path}\n")
                if sys.stdout.isatty() and should_emit_beep(snapshot, self.tick, self.last_beep_tick):
                    sys.stdout.write("\a")
                    self.last_beep_tick = self.tick
                sys.stdout.write("\x1b[J")
                sys.stdout.flush()
                time.sleep(1 / max(1, self.state.fps))
                self.tick += 1
        finally:
            sys.stdout.write("\x1b[?25h\n")
            sys.stdout.flush()


def install_signal_handlers(state: FaceState) -> None:
    def _handler(signum, frame):
        state.apply({"shutdown": True, "text": f"caught signal {signum}"})

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)


def send_payload(socket_path: str, payload: dict[str, Any]) -> dict[str, Any]:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        for _ in range(25):
            try:
                sock.connect(socket_path)
                break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError(f"Could not connect to socket: {socket_path}")
        file = sock.makefile("rwb")
        file.write((json.dumps(payload) + "\n").encode("utf-8"))
        file.flush()
        return json.loads(file.readline().decode("utf-8"))


def demo_loop(socket_path: str) -> None:
    sequence = [
        {"emotion": "happy", "say": "boot sequence complete", "pulse": True},
        {"stream_start": True},
        {"stream_chunk": "checking left flank... "},
        {"stream_chunk": "parsing your instructions... "},
        {"stream_chunk": "ready to perform!"},
        {"stream_end": True},
        {"emotion": "neutral", "look": 0, "text": "demo idle"},
    ]
    for payload in sequence:
        send_payload(socket_path, payload)
        time.sleep(1.2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Live ASCII face that accepts emotion commands over a Unix socket.")
    parser.add_argument("--socket", default=DEFAULT_SOCKET, help="Unix socket path for control messages")
    parser.add_argument("--fps", type=int, default=12, help="Frames per second")
    parser.add_argument("--demo", action="store_true", help="Run a short built-in demo after startup")
    args = parser.parse_args()

    state = FaceState(fps=args.fps)
    install_signal_handlers(state)
    server = FaceServer(args.socket, state)
    server.start()

    if args.demo:
        threading.Thread(target=demo_loop, args=(args.socket,), daemon=True).start()

    TerminalFace(state, args.socket).draw()
    server.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
