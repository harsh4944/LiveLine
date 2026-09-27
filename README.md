# LiveLine — setup

LiveLine
On-Device Live Captioning & Translation for Snapdragon-Powered HP PCs
Snapdragon® AI Lab Build & Present Challenge — Solution Submission
Problem
Real-time captioning and translation today depend on cloud speech APIs. This creates three recurring failures: sensitive audio (meetings, interviews, classrooms) leaves the device and is exposed to third parties; the experience breaks entirely without a stable internet connection, which rules out rural schools, field teams, and low-bandwidth regions across India; and continuous cloud usage adds latency and per-minute cost that does not scale.
Solution
LiveLine is a fully offline captioning and translation assistant that runs entirely on a Snapdragon-powered HP PC's NPU. It transcribes speech in real time using Whisper (deployed via Qualcomm AI Hub), displays live captions in an always-on-top overlay, and optionally translates them — all without an internet connection, and without any audio leaving the device.
●	Offline-first: works with zero connectivity, demonstrated live in airplane mode.
●	Private by design: all inference happens on-device; nothing is uploaded.
●	Built for accessibility: serves hearing-impaired users, non-native speakers, and low-bandwidth classrooms.
Architecture
Mic input is captured in short chunks and passed to Whisper (Whisper-Tiny / Whisper-Small-Quantized), running on the Snapdragon NPU via Qualcomm AI Hub's precompiled QNN ONNX models and the ONNX Runtime QNN execution provider. Transcribed text renders immediately in a caption overlay; an optional on-device machine-translation layer converts it into the selected target language before display.
Why the Snapdragon NPU
●	Latency: the Whisper encoder runs in roughly 21 ms on NPU, keeping captions close to real time.
●	Battery life: NPU inference draws far less power than sustained cloud streaming and radio use.
●	Privacy: no audio or transcript ever leaves the laptop.
●	Reach: works identically in a connected city office or an offline rural classroom.
Technical Implementation
●	Speech-to-text: Whisper-Tiny / Whisper-Small-Quantized from Qualcomm AI Hub, deployed via precompiled QNN ONNX binaries for the target Snapdragon chipset.
●	Inference runtime: ONNX Runtime with the QNN execution provider — NPU-accelerated, no cloud round-trip.
●	Translation: a lightweight on-device MT model, kept optional so the core offline pipeline stays fast.
●	Interface: an always-on-top caption overlay with language selection and continuous transcript export.
●	Benchmarking: NPU vs. CPU inference latency measured directly on the target Snapdragon-powered HP PC.
Demo & Impact
The submitted demo shows LiveLine running fully offline — captured in airplane mode — in a realistic meeting or lecture scenario, alongside a side-by-side NPU vs. CPU latency comparison. The target impact is accessibility at the point of need: hearing-impaired users and non-native speakers get live captions without any cloud dependency, and low-bandwidth classrooms or field teams get a captioning tool that works regardless of connectivity.
Roadmap
●	Additional Indian language support for the translation layer.
●	A sign-language recognition module as a complementary accessibility channel.
●	A mobile / Snapdragon handset port.


## Step 1: Get it running today (CPU, no Snapdragon setup needed)

```bash
pip install -r requirements.txt
python live_demo.py --backend cpu --chunk 4
```

Speak into your mic — you'll see timestamped captions print live, and a
`transcript.txt` file will be written. This lets you start building the
overlay UI (Day 2) immediately, without waiting on NPU setup.

## Step 2: Confirm your exact Snapdragon chipset

```powershell
# Windows PowerShell
Get-CimInstance Win32_Processor | Select-Object Name
```

Match the result against the chipset table on the model page, e.g.:
https://aihub.qualcomm.com/mobile/models/whisper_tiny

You need the exact chipset name (X Elite / X2 Elite / 8 Gen 3, etc.) —
the pre-compiled NPU binaries are chipset-specific.

## Step 3: Install the NPU path and confirm its real API

```bash
pip install "qai_hub_models[whisper_tiny_en]"
```

Sign up at https://aihub.qualcomm.com, create an API token under
Account → Settings → API Token, then:

```bash
qai-hub configure --api_token YOUR_TOKEN
```

Before touching `engine.py`, look at what's actually installed —
the library's internal API has shifted across versions, so trust your
installed copy over any remembered snippet:

```bash
python -m qai_hub_models.models.whisper_tiny_en.demo --help
python -c "import qai_hub_models.models.whisper_tiny_en.demo as d; print(d.__file__)"
```

Open the file that second command prints — it's short and shows exactly
how the demo loads the model and calls transcription. Copy those two
calls into the `TODO`s in `engine.py`'s `QNNWhisperEngine`.

## Step 4: Run the NPU version and capture your benchmark

```bash
python live_demo.py --backend qnn --chunk 4
```

The avg latency printed at the end, next to the CPU run's number, is
your NPU vs. CPU benchmark for the Technical Implementation slide.

## Step 5: Wire into a UI (Day 2)

`engine.py`'s `transcribe_chunk()` is the only call your UI needs —
feed it mic chunks, display the returned text. A simple always-on-top
window (Tkinter, or PyQt for nicer styling) works fine; no need for
anything elaborate.

## Rquirement 
# --- Works immediately, CPU only (use this to build/test the app today) ---
sounddevice==0.4.7
numpy==1.26.4
openai-whisper==20231117

# --- NPU-accelerated path for your final Snapdragon submission ---
# Install these once you've confirmed your exact chipset (see README Step 3).
# qai-hub-models[whisper-tiny]
# onnxruntime-qnn


