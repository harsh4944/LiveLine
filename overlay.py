"""
overlay.py — Always-on-top caption overlay for LiveLine.

A borderless, draggable window that shows live captions as they're
transcribed, with Start/Stop, Save Transcript, and a language selector
stubbed in for the translation layer. Runs the same engine.py backends
as live_demo.py — audio capture and inference happen on a background
thread so the UI never freezes.

Usage:
    python overlay.py --backend cpu --chunk 4
    python overlay.py --backend qnn --chunk 4   # after engine.py TODOs are filled in
"""

import argparse
import queue
import threading
import time
from datetime import datetime

import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import font as tkfont

from engine import get_engine

SAMPLE_RATE = 16000
CHANNELS = 1
MAX_LINES = 6

LANGUAGES = ["Original", "Hindi", "Spanish", "French"]


class CaptionOverlay:
    def __init__(self, root, backend, chunk_seconds, transcript_path):
        self.root = root
        self.backend = backend
        self.chunk_seconds = chunk_seconds
        self.transcript_path = transcript_path

        self.engine = None
        self.running = False
        self.audio_stream = None
        self.audio_queue = queue.Queue()
        self.lines = []
        self.latencies = []

        self._build_window()

    # ---------- UI ----------

    def _build_window(self):
        r = self.root
        r.title("LiveLine")
        r.attributes("-topmost", True)
        r.configure(bg="#0D1B2A")
        r.geometry("900x260+80+80")
        r.minsize(500, 160)

        caption_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        status_font = tkfont.Font(family="Segoe UI", size=10)

        # Drag-to-move (borderless-style, but keep native chrome for demo reliability)
        header = tk.Frame(r, bg="#0D1B2A")
        header.pack(fill="x", padx=12, pady=(10, 0))

        tk.Label(header, text="LiveLine", fg="#5DA9E9", bg="#0D1B2A",
                 font=("Segoe UI", 12, "bold")).pack(side="left")

        self.status_var = tk.StringVar(value="Stopped")
        tk.Label(header, textvariable=self.status_var, fg="#9FB3C8", bg="#0D1B2A",
                 font=status_font).pack(side="left", padx=12)

        tk.Label(header, text="Translate to:", fg="#9FB3C8", bg="#0D1B2A",
                 font=status_font).pack(side="right", padx=(0, 4))
        self.lang_var = tk.StringVar(value=LANGUAGES[0])
        tk.OptionMenu(header, self.lang_var, *LANGUAGES).pack(side="right")

        # Caption area
        self.caption_var = tk.StringVar(value="Press Start and begin speaking...")
        caption_label = tk.Label(
            r, textvariable=self.caption_var, fg="#F5F7FA", bg="#0D1B2A",
            font=caption_font, wraplength=860, justify="left", anchor="w",
        )
        caption_label.pack(fill="both", expand=True, padx=14, pady=10)

        # Controls
        controls = tk.Frame(r, bg="#0D1B2A")
        controls.pack(fill="x", padx=12, pady=(0, 10))

        self.start_btn = tk.Button(controls, text="Start", command=self.toggle,
                                    bg="#2E7DD1", fg="white", relief="flat", padx=14, pady=4)
        self.start_btn.pack(side="left")

        tk.Button(controls, text="Save Transcript", command=self.save_transcript,
                  bg="#1B2A4A", fg="white", relief="flat", padx=14, pady=4).pack(side="left", padx=8)

        self.latency_var = tk.StringVar(value="")
        tk.Label(controls, textvariable=self.latency_var, fg="#6B7C93", bg="#0D1B2A",
                 font=status_font).pack(side="right")

        r.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- Engine lifecycle ----------

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        self.status_var.set("Loading model...")
        self.root.update_idletasks()
        threading.Thread(target=self._start_engine_and_stream, daemon=True).start()

    def _start_engine_and_stream(self):
        if self.engine is None:
            self.engine = get_engine(self.backend)

        self.running = True
        self.root.after(0, lambda: self.status_var.set("Listening..."))
        self.root.after(0, lambda: self.start_btn.config(text="Stop"))

        def audio_callback(indata, frames, t, status):
            self.audio_queue.put(indata.copy())

        block_frames = int(SAMPLE_RATE * 0.1)
        self.audio_stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="float32",
            blocksize=block_frames, callback=audio_callback,
        )
        self.audio_stream.start()

        blocks_per_chunk = int(self.chunk_seconds / 0.1)
        while self.running:
            blocks = []
            for _ in range(blocks_per_chunk):
                if not self.running:
                    break
                try:
                    blocks.append(self.audio_queue.get(timeout=0.5))
                except queue.Empty:
                    continue
            if not blocks or not self.running:
                continue

            chunk = np.concatenate(blocks, axis=0).flatten()
            if np.abs(chunk).mean() < 0.003:
                continue  # skip near-silence

            text, latency_ms = self.engine.transcribe_chunk(chunk, SAMPLE_RATE)
            if text:
                self._on_caption(text, latency_ms)

    def _on_caption(self, text, latency_ms):
        self.latencies.append(latency_ms)
        stamp = datetime.now().strftime("%H:%M:%S")
        self.lines.append(f"[{stamp}] {text}")
        self.lines = self.lines[-MAX_LINES:]

        def update():
            self.caption_var.set("\n".join(self.lines))
            avg = sum(self.latencies) / len(self.latencies)
            self.latency_var.set(f"avg latency: {avg:.0f} ms  |  backend: {self.backend}")

        self.root.after(0, update)

        with open(self.transcript_path, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {text}\n")

    def stop(self):
        self.running = False
        if self.audio_stream is not None:
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None
        self.status_var.set("Stopped")
        self.start_btn.config(text="Start")

    def save_transcript(self):
        self.status_var.set(f"Saved -> {self.transcript_path}")

    def on_close(self):
        self.stop()
        self.root.destroy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["cpu", "qnn"], default="cpu")
    parser.add_argument("--chunk", type=float, default=4.0)
    parser.add_argument("--transcript-out", default="transcript.txt")
    args = parser.parse_args()

    root = tk.Tk()
    CaptionOverlay(root, args.backend, args.chunk, args.transcript_out)
    root.mainloop()


if __name__ == "__main__":
    main()
