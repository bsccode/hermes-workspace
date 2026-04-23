#!/usr/bin/env python3
import argparse
import json
import socket
import sys
import time
from pathlib import Path
from typing import Optional

DEFAULT_SOCKET = "/tmp/ascii-face-agent.sock"


def send_message(socket_path: str, payload: dict) -> dict:
    if not Path(socket_path).exists():
        raise FileNotFoundError(f"Socket does not exist: {socket_path}")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(socket_path)
        file = sock.makefile("rwb")
        file.write((json.dumps(payload) + "\n").encode("utf-8"))
        file.flush()
        response = file.readline().decode("utf-8").strip()
        return json.loads(response)


def stream_stdin(socket_path: str, delay: float, clear: bool, auto_emote: bool, beep: bool, clear_after: Optional[float]) -> dict:
    start_payload = {"stream_start": True, "clear": clear, "auto_emote": auto_emote, "beep": beep}
    send_message(socket_path, start_payload)
    while True:
        chunk = sys.stdin.read(1)
        if chunk == "":
            break
        send_message(socket_path, {"stream_chunk": chunk, "auto_emote": auto_emote, "beep": beep})
        if delay > 0:
            time.sleep(delay)
    end_payload = {"stream_end": True, "auto_emote": auto_emote, "beep": beep}
    if clear_after is not None:
        end_payload["clear_after"] = clear_after
    return send_message(socket_path, end_payload)


def build_payload(args: argparse.Namespace) -> dict:
    payload = {}
    field_map = {
        "emotion": args.emotion,
        "say": args.say,
        "text": args.text,
        "look": args.look,
        "mouth": args.mouth,
        "duration": args.duration,
        "text_duration": args.text_duration,
        "stream_chunk": args.stream_chunk,
        "clear_after": args.clear_after,
    }
    for key, value in field_map.items():
        if value is not None:
            payload[key] = value
    if args.blink:
        payload["blink"] = True
    if args.pulse:
        payload["pulse"] = True
    if args.reset:
        payload["reset"] = True
    if args.shutdown:
        payload["shutdown"] = True
    if args.stream_start:
        payload["stream_start"] = True
        payload["clear"] = args.clear
        payload["auto_emote"] = args.auto_emote
    if args.stream_end:
        payload["stream_end"] = True
        payload["auto_emote"] = args.auto_emote
    if args.stream_chunk is not None and "auto_emote" not in payload:
        payload["auto_emote"] = args.auto_emote
    if args.auto_emote is False and "auto_emote" not in payload:
        payload["auto_emote"] = False
    if args.no_beep:
        payload["beep"] = False
    elif args.beep:
        payload["beep"] = True
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Send control messages to the ASCII face server.")
    parser.add_argument("--socket", default=DEFAULT_SOCKET, help="Unix socket path")
    parser.add_argument("--emotion", help="Set emotion")
    parser.add_argument("--say", help="Display text and animate talking")
    parser.add_argument("--text", help="Display status text without talking")
    parser.add_argument("--look", type=int, choices=[-1, 0, 1], help="Look left (-1), center (0), or right (1)")
    parser.add_argument("--blink", action="store_true", help="Force a blink")
    parser.add_argument("--pulse", action="store_true", help="Pulse the face border briefly")
    parser.add_argument("--mouth", help="Override mouth shape")
    parser.add_argument("--duration", type=float, help="Speech animation duration")
    parser.add_argument("--text-duration", type=float, help="Visible text duration")
    parser.add_argument("--stream-start", action="store_true", help="Start streaming transcript mode")
    parser.add_argument("--stream-chunk", help="Append a chunk of streamed text")
    parser.add_argument("--stream-end", action="store_true", help="Finish streaming transcript mode")
    parser.add_argument("--stream-stdin", action="store_true", help="Read stdin one character at a time and stream it to the face")
    parser.add_argument("--stream-delay", type=float, default=0.0, help="Delay between streamed stdin characters")
    parser.add_argument("--clear-after", type=float, help="Seconds to keep streamed text visible after stream_end")
    parser.add_argument("--clear", dest="clear", action="store_true", default=True, help="Clear existing transcript when starting a stream")
    parser.add_argument("--no-clear", dest="clear", action="store_false", help="Preserve existing transcript when starting a stream")
    parser.add_argument("--auto-emote", dest="auto_emote", action="store_true", default=True, help="Infer emotion from streamed or spoken text")
    parser.add_argument("--no-auto-emote", dest="auto_emote", action="store_false", help="Disable automatic emotion inference")
    parser.add_argument("--beep", dest="beep", action="store_true", default=True, help="Emit terminal bell beeps while streaming/speaking")
    parser.add_argument("--no-beep", dest="no_beep", action="store_true", help="Disable terminal bell beeps")
    parser.add_argument("--reset", action="store_true", help="Reset to neutral")
    parser.add_argument("--shutdown", action="store_true", help="Stop the face server")
    parser.add_argument("--json", help="Raw JSON payload string to send instead of flags")
    args = parser.parse_args()

    if args.stream_stdin:
        response = stream_stdin(args.socket, args.stream_delay, args.clear, args.auto_emote, not args.no_beep, args.clear_after)
    elif args.json:
        response = send_message(args.socket, json.loads(args.json))
    else:
        payload = build_payload(args)
        if not payload:
            parser.error("No command given. Use flags, --stream-stdin, or --json.")
        response = send_message(args.socket, payload)

    sys.stdout.write(json.dumps(response, indent=2) + "\n")
    return 0 if response.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
