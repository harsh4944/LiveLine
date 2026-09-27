# LiveLine — setup

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


