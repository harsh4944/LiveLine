"""
live_demo.py — Console live-captioning loop for LiveLine.

Records fixed-length chunks from the mic, transcribes each with the
chosen engine, prints captions as they arrive, and saves a full
transcript. This is the console proof-of-concept — wire the same
engine calls into a GUI overlay for Day 2.

Usage:
    python live_demo.py --backend cpu --chunk 4
    python live_demo.py --backend qnn --chunk 4   # after engine.py TODOs are filled in
"""

import argparse
import queue
import time
from datetime import datetime

import numpy as np
import sounddevice as sd

from engine import get_engine

SAMPLE_RATE = 16000
CHANNELS = 1


def record_chunks(chunk_seconds, sample_rate=SAMPLE_RATE):
    """Yields consecutive audio chunks (float32 numpy arrays) from the default mic."""
    q = queue.Queue()

    def callback(indata, frames, t, status):
        if status:
            print(f"[audio] {status}")
        q.put(indata.copy())

    block_frames = int(sample_rate * 0.1)  # 100ms callback blocks
    blocks_per_chunk = int(chunk_seconds / 0.1)

    with sd.InputStream(
        samplerate=sample_rate,
        channels=CHANNELS,
        dtype="float32",
        blocksize=block_frames,
        callback=callback,
    ):
        while True:
            blocks = [q.get() for _ in range(blocks_per_chunk)]
            chunk = np.concatenate(blocks, axis=0).flatten()
            yield chunk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["cpu", "qnn"], default="cpu")
    parser.add_argument("--chunk", type=float, default=4.0, help="seconds per caption chunk")
    parser.add_argument("--language", default=None, help="e.g. 'en', 'hi' (cpu backend only)")
    parser.add_argument("--transcript-out", default="transcript.txt")
    args = parser.parse_args()

    print(f"[setup] loading '{args.backend}' engine ...")
    engine = get_engine(args.backend, language=args.language) if args.backend == "cpu" else get_engine(args.backend)

    print(f"[ready] listening in {args.chunk}s chunks — Ctrl+C to stop.\n")

    latencies = []
    with open(args.transcript_out, "a", encoding="utf-8") as logf:
        try:
            for chunk in record_chunks(args.chunk):
                # skip near-silent chunks so we don't waste inference on dead air
                if np.abs(chunk).mean() < 0.003:
                    continue

                text, latency_ms = engine.transcribe_chunk(chunk, SAMPLE_RATE)
                if not text:
                    continue

                latencies.append(latency_ms)
                stamp = datetime.now().strftime("%H:%M:%S")
                line = f"[{stamp}] {text}"
                print(line)
                logf.write(line + "\n")
                logf.flush()
        except KeyboardInterrupt:
            pass

    if latencies:
        avg = sum(latencies) / len(latencies)
        print(f"\n[stats] chunks transcribed: {len(latencies)} | avg latency: {avg:.1f} ms")
        print("        (capture this number, and re-run with --backend qnn, for your")
        print("         Technical Implementation slide's NPU vs CPU benchmark.)")
    print(f"[saved] transcript -> {args.transcript_out}")


if __name__ == "__main__":
    main()
