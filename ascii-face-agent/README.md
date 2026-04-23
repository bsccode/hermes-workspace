ASCII Face Agent

A live terminal face for Linux/macOS that listens on a Unix socket so another agent can emote through it.

What it does
- draws a blinking ASCII face in a regular terminal
- accepts JSON commands over a Unix domain socket
- supports one-shot speech plus streamed transcript updates
- auto-inferrs a rough emotion from the text unless you explicitly set one
- clears streamed text shortly after the stream ends by default
- emits simple terminal bell beeps while text is actively streaming/speaking
- uses only Python standard library

Files
- /Users/blake/hermes-workspace/ascii-face-agent/face_server.py
- /Users/blake/hermes-workspace/ascii-face-agent/face_client.py
- /Users/blake/hermes-workspace/ascii-face-agent/test_face_server.py

Run it
1. Start the face in a terminal:
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_server.py

2. Optional: start with the built-in demo:
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_server.py --demo

3. In another terminal, send commands:
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --emotion happy --say "hello human"
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --stream-start
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --stream-chunk "I am thinking through this... "
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --stream-chunk "almost there!"
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --stream-end --clear-after 0.6
   python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --shutdown

Fast path for agent output
Pipe text directly into the face as a live transcript:
   printf 'Let me think... okay, I have it!' | python3 /Users/blake/hermes-workspace/ascii-face-agent/face_client.py --stream-stdin --stream-delay 0.02 --clear-after 0.8

Socket protocol
Default socket:
- /tmp/ascii-face-agent.sock

Each message is one JSON object followed by a newline.

Example payloads
{"emotion":"happy","say":"I can talk with my face now"}
{"stream_start":true}
{"stream_chunk":"Let me think through that... "}
{"stream_chunk":"done!"}
{"stream_end":true,"clear_after":0.8}
{"blink":true}
{"pulse":true}
{"mouth":"[___]","text":"custom mouth"}
{"reset":true}
{"shutdown":true}

Supported emotions
- neutral
- happy
- sad
- angry
- surprised
- thinking
- sleepy
- excited

Auto-emote behavior
- text with "hmm", "let me", "analy...", "reason..." tends to thinking
- text with "!", "solved", "awesome", "done" tends to excited
- text with "sorry", "failed", "error" tends to sad
- text with "warning", "danger", "critical" tends to angry
- text with "?", "wow", "unexpected" tends to surprised

Typical agent integration
Python example:

import json
import socket

messages = [
    {"stream_start": True},
    {"stream_chunk": "Let me inspect that... "},
    {"stream_chunk": "I found the issue!"},
    {"stream_end": True},
]

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.connect("/tmp/ascii-face-agent.sock")
    file = sock.makefile("rwb")
    for payload in messages:
        file.write((json.dumps(payload) + "\n").encode())
        file.flush()
        print(file.readline().decode().strip())

TTS next step
- Stream the transcript to this face
- Send the same text chunks to a TTS engine
- Use chunk timing or phoneme callbacks later to drive mouth shapes more accurately

Notes
- The face redraws continuously and blinks on its own.
- While speaking, the eyes drift slightly for a more alive look.
- During streaming, the transcript stays visible with a live cursor, then clears shortly after stream_end.
- Explicit emotion overrides auto-emote.
- The speaking/streaming loop emits terminal bell beeps by default; use --no-beep if you hate it.
- The app is meant for Unix-like systems because it uses Unix domain sockets and ANSI terminal control.
