"""
engine.py — Speech-to-text backend for LiveLine.

Two backends behind one interface, so you can build the UI now and swap
the engine for your final Snapdragon submission without touching app code.

  CPUWhisperEngine  -> runs today, on any machine, via openai-whisper.
                       Use this while you build/test the caption UI.

  QNNWhisperEngine  -> runs Whisper on the Snapdragon NPU via Qualcomm's
                       qai_hub_models package. This is what you submit.
                       NOT wired up blind: qai_hub_models' internal API
                       (class names, method signatures) has changed
                       across releases, so Step 3 in the README has you
                       confirm the real signature on your machine first,
                       then fill in the two TODOs below. This keeps you
                       from shipping code against a guessed API.
"""

import time
import numpy as np


class CPUWhisperEngine:
    """Baseline engine — works out of the box, no Snapdragon-specific setup."""

    def __init__(self, model_size="tiny", language=None):
        import whisper  # openai-whisper
        print(f"[engine] loading openai-whisper '{model_size}' on CPU ...")
        self.model = whisper.load_model(model_size)
        self.language = language

    def transcribe_chunk(self, audio_f32, sample_rate=16000):
        """audio_f32: 1-D float32 numpy array in [-1, 1], mono, 16kHz."""
        t0 = time.time()
        result = self.model.transcribe(
            audio_f32,
            language=self.language,
            fp16=False,
            condition_on_previous_text=False,
        )
        latency_ms = (time.time() - t0) * 1000
        return result["text"].strip(), latency_ms


class QNNWhisperEngine:
    """
    NPU-accelerated engine for the actual Snapdragon submission.

    Setup (do this once you know your chipset — see README Step 3):
        pip install "qai_hub_models[whisper_tiny_en]"
        qai-hub configure --api_token YOUR_TOKEN

    Before filling in the TODOs, run this on your machine to see the
    real, currently-installed API for your package version:
        python -c "import qai_hub_models.models.whisper_tiny_en as m; help(m)"
        python -m qai_hub_models.models.whisper_tiny_en.demo --help

    That demo module's source (find it with `python -c "import
    qai_hub_models.models.whisper_tiny_en.demo as d; print(d.__file__)"`)
    shows the exact load + transcribe calls for your installed version —
    copy the real ones into the two TODOs below rather than guessing.
    """

    def __init__(self, device_chipset="qualcomm-snapdragon-x-elite"):
        # TODO: replace with the real model/app construction from demo.py,
        # e.g. something like:
        #   from qai_hub_models.models.whisper_tiny_en.model import WhisperTinyEn
        #   from qai_hub_models.models._shared.whisper.app import WhisperApp
        #   self.app = WhisperApp(WhisperTinyEn.from_pretrained())
        raise NotImplementedError(
            "Fill this in using your installed qai_hub_models demo.py as "
            "the reference — see the class docstring above."
        )

    def transcribe_chunk(self, audio_f32, sample_rate=16000):
        # TODO: replace with the real call, e.g.
        #   t0 = time.time()
        #   text = self.app.transcribe(audio_f32, sample_rate)
        #   latency_ms = (time.time() - t0) * 1000
        #   return text.strip(), latency_ms
        raise NotImplementedError


def get_engine(backend="cpu", **kwargs):
    if backend == "cpu":
        return CPUWhisperEngine(**kwargs)
    if backend == "qnn":
        return QNNWhisperEngine(**kwargs)
    raise ValueError(f"Unknown backend: {backend}")
