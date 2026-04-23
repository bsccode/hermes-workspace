ASCII Face Agent: Code Explanation

Overview
This project is a terminal-based ASCII character controlled over a Unix domain socket. One process owns the face renderer. Other processes send JSON messages to update state, stream transcript text, and trigger emotions.

Main files
- /Users/blake/hermes-workspace/ascii-face-agent/face_server.py
  Core app. Holds state, renders frames, accepts socket messages, handles streaming/emotion logic.
- /Users/blake/hermes-workspace/ascii-face-agent/face_client.py
  Convenience CLI for sending commands to the face. Useful for manual testing and agent integration.
- /Users/blake/hermes-workspace/ascii-face-agent/test_face_server.py
  Unit tests for streaming, auto-emotion inference, render behavior, beep cadence, and socket round-trip behavior.
- /Users/blake/hermes-workspace/ascii-face-agent/README.md
  Usage instructions and protocol examples.

How the server is structured
1. FaceState
   This is the central mutable state object.

   It stores:
   - emotion
   - visible text/transcript
   - look direction
   - blink timing
   - speaking timing
   - pulse timing
   - whether streaming is active
   - whether auto-emote is enabled
   - whether beep effects are enabled

   Important methods:
   - snapshot()
     Returns a render-safe view of the current state.
   - apply(payload)
     Applies one incoming JSON command.

2. infer_emotion_from_text(text)
   Lightweight heuristic emotion classifier.

   Current behavior:
   - “hmm”, “let me”, “reason”, etc. -> thinking
   - “done!”, “awesome”, “solved”, etc. -> excited
   - “sorry”, “failed”, “error” -> sad
   - “warning”, “danger”, “critical” -> angry
   - “?”, “unexpected”, “wow” -> surprised

   This is intentionally simple and cheap. It is good enough for live terminal animation without adding dependencies.

3. render_face(snapshot, tick)
   Converts state into the actual ASCII frame.

   It handles:
   - brows / eyes / mouth by emotion
   - blink frames
   - look direction
   - talking mouth animation
   - streaming cursor
   - transcript rendering

4. FaceServer
   Owns the Unix socket.

   Responsibilities:
   - create and bind the socket
   - accept incoming connections
   - read one JSON object per line
   - pass messages to FaceState.apply()
   - return the updated state as a JSON response

5. TerminalFace
   The render loop.

   Responsibilities:
   - redraw the face at the configured FPS
   - trigger occasional autonomous blinking
   - emit terminal bell beeps while streaming/speaking
   - clear/redraw the terminal using ANSI escape sequences

Protocol design
Messages are newline-delimited JSON objects.

Typical commands
- {"emotion": "happy"}
- {"say": "hello"}
- {"stream_start": true}
- {"stream_chunk": "Let me think... "}
- {"stream_end": true, "clear_after": 0.8}
- {"shutdown": true}

Why Unix sockets
A Unix domain socket is a good fit here because:
- local-only by default
- simple to script
- low overhead
- no extra networking stack complexity
- works well on macOS and Linux

Why the text used to stick around
Earlier, stream_end stopped streaming but left the transcript visible for a long display window. That made the face feel “stuck” with old text. The current logic instead uses a short post-stream visibility window and then clears naturally.

How the beep effect works
The sound is the terminal bell character: \a

That means:
- some terminals play a short beep
- some flash visually instead
- some ignore it depending on terminal settings

The code intentionally emits beeps only on a cadence, not every frame, so it feels more like retro machine chatter instead of a continuous alarm.

Current limitations
- emotion inference is heuristic, not semantic
- mouth movement is timing-based, not phoneme-based
- terminal bell quality depends on the terminal emulator
- no real audio synthesis yet

Best next upgrades
1. Add a face bridge process
   One process that accepts streamed agent output and fans it out to:
   - face socket
   - TTS engine
   - optional conversation log

2. Add richer sound generation
   Instead of \a only, generate tiny retro synth chirps or filtered beeps.

3. Add viseme support
   If TTS provides phoneme/viseme timing, use that to drive mouth shapes.

4. Add personality presets
   Different idle behavior, blink rate, and emotion bias for different characters.

Testing strategy
Tests currently cover:
- render output includes expected transcript/cursor info
- stream chunks accumulate correctly
- stream end clears text after configured delay
- auto-emotion inference returns expected moods
- beep emission logic only fires while active
- Unix socket control path works end to end

Git note
This project lives inside the larger hermes-workspace repository as:
- /Users/blake/hermes-workspace/ascii-face-agent

So committing it will add the whole feature directory into the workspace repo rather than pushing a separate standalone repo.
