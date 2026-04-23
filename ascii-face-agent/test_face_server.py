#!/usr/bin/env python3
import json
import socket
import tempfile
import time
import unittest
from pathlib import Path

import face_server


class FaceServerTests(unittest.TestCase):
    def test_apply_and_render(self):
        state = face_server.FaceState()
        snapshot = state.apply({"emotion": "happy", "say": "hello", "look": 1, "pulse": True})
        frame = face_server.render_face(snapshot, tick=1)
        self.assertIn("hello", frame)
        self.assertIn("commands: emotion, say, blink", frame)
        self.assertEqual(snapshot["emotion"], "happy")
        self.assertEqual(snapshot["look_x"], 1)

    def test_streaming_chunks_accumulate_transcript_and_speaking(self):
        state = face_server.FaceState()
        state.apply({"stream_start": True, "text": ""})
        first = state.apply({"stream_chunk": "hello"})
        second = state.apply({"stream_chunk": " there!"})
        final = state.apply({"stream_end": True})

        self.assertEqual(first["text"], "hello")
        self.assertEqual(second["text"], "hello there!")
        self.assertTrue(second["speaking"])
        self.assertEqual(second["emotion"], "excited")
        self.assertFalse(final["streaming"])
        self.assertEqual(final["text"], "hello there!")

    def test_stream_end_clears_text_after_short_delay(self):
        state = face_server.FaceState()
        state.apply({"stream_start": True})
        state.apply({"stream_chunk": "temporary transcript"})
        state.apply({"stream_end": True, "clear_after": 0.05, "duration": 0.01})
        time.sleep(0.08)
        self.assertEqual(state.snapshot()["text"], "")

    def test_auto_emotion_inference_prefers_text_cues(self):
        self.assertEqual(face_server.infer_emotion_from_text("I solved it!"), "excited")
        self.assertEqual(face_server.infer_emotion_from_text("hmm, let me think about that"), "thinking")
        self.assertEqual(face_server.infer_emotion_from_text("sorry, that failed"), "sad")
        self.assertEqual(face_server.infer_emotion_from_text("warning: danger detected"), "angry")
        self.assertEqual(face_server.infer_emotion_from_text("what?"), "surprised")

    def test_render_includes_stream_cursor(self):
        state = face_server.FaceState()
        snapshot = state.apply({"stream_start": True, "stream_chunk": "streaming live"})
        frame = face_server.render_face(snapshot, tick=2)
        self.assertIn("streaming live", frame)
        self.assertIn("▋", frame)

    def test_beep_cadence_only_during_active_streaming(self):
        state = face_server.FaceState()
        state.apply({"stream_start": True, "stream_chunk": "beep"})
        streaming_snapshot = state.snapshot()
        self.assertTrue(face_server.should_emit_beep(streaming_snapshot, tick=4, last_beep_tick=0))
        self.assertFalse(face_server.should_emit_beep(streaming_snapshot, tick=5, last_beep_tick=4))
        self.assertFalse(face_server.should_emit_beep({**streaming_snapshot, "streaming": False, "speaking": False}, tick=8, last_beep_tick=4))

    def test_unix_socket_round_trip(self):
        state = face_server.FaceState()
        with tempfile.TemporaryDirectory() as tmpdir:
            socket_path = str(Path(tmpdir) / "face.sock")
            server = face_server.FaceServer(socket_path, state)
            server.start()
            for _ in range(50):
                if Path(socket_path).exists():
                    break
                time.sleep(0.05)
            else:
                self.fail("socket was not created")

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(socket_path)
                file = sock.makefile("rwb")
                file.write((json.dumps({"stream_start": True}) + "\n").encode())
                file.flush()
                start_response = json.loads(file.readline().decode())
                self.assertTrue(start_response["ok"])
                self.assertTrue(start_response["state"]["streaming"])

                file.write((json.dumps({"stream_chunk": "working on it..."}) + "\n").encode())
                file.flush()
                chunk_response = json.loads(file.readline().decode())
                self.assertTrue(chunk_response["ok"])
                self.assertEqual(chunk_response["state"]["emotion"], "thinking")
                self.assertIn("working on it", chunk_response["state"]["text"])

                file.write((json.dumps({"shutdown": True}) + "\n").encode())
                file.flush()
                json.loads(file.readline().decode())

            server.join(timeout=2)
            self.assertFalse(server.is_alive())
            self.assertFalse(Path(socket_path).exists())


if __name__ == "__main__":
    unittest.main()
