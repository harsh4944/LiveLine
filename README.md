# 🎙️ LiveLine

## On-Device Live Captioning & Translation for Snapdragon-Powered HP PCs

**LiveLine** is an offline-first, privacy-focused live captioning and translation assistant designed for **Snapdragon-powered HP PCs**.

It transcribes speech in real time and optionally translates it into another language, with the goal of running AI inference **locally on the Snapdragon NPU** — without sending audio to the cloud.

> 🏆 Built for the **Snapdragon® AI Lab Build & Present Challenge by Qualcomm**

---

## ✨ Features

* 🎤 Real-time speech-to-text
* ⚡ Snapdragon NPU acceleration
* 🔒 Privacy-focused on-device inference
* 🌐 Optional on-device translation
* ✈️ Designed to work completely offline
* 🖥️ Always-on-top caption overlay
* 📄 Continuous transcript export
* 📊 CPU vs NPU latency benchmarking
* ♿ Designed with accessibility use cases in mind

---

# 🧩 Problem

Real-time captioning and translation solutions often depend on cloud-based speech APIs.

This creates three recurring challenges:

### 🔐 Privacy Risk

Meetings, interviews, classrooms, and other conversations can contain sensitive information. Sending audio to external servers creates additional privacy concerns.

### 🌐 Internet Dependency

Cloud-based captioning can become unavailable when connectivity is poor or completely unavailable.

This can affect:

* Rural classrooms
* Field teams
* Low-bandwidth regions
* Travel and offline environments

### ⏱️ Latency & Cost

Cloud inference introduces network round trips and continuous usage costs, which can become difficult to scale for long-running applications.

---

# 💡 Solution

**LiveLine brings live captioning directly onto the user's PC.**

### Offline-first

LiveLine is designed to operate without an active internet connection.

### Privacy-focused

Speech recognition is performed locally, avoiding the need for a cloud speech API in the core pipeline.

### Accessibility

LiveLine is designed to support:

* Hearing-impaired users
* Non-native speakers
* Students
* Teachers
* Meeting participants
* Field teams
* Low-connectivity communities

---

# 🏗️ Architecture

```text
┌─────────────────┐
│   Microphone    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Audio Chunks  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│     Whisper STT         │
│  Snapdragon NPU / CPU   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Live Transcript │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Optional Translation    │
│   On-Device MT Model    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Caption Overlay │
└─────────────────┘
```

---

# ⚡ Why the Snapdragon NPU?

LiveLine is designed around local AI inference, making the Snapdragon NPU an important part of the system.

### 🚀 Low Latency

NPU acceleration is intended to reduce inference latency and keep captions close to real time.

### 🔋 Efficient AI Inference

Running supported AI workloads locally on the NPU can reduce dependence on cloud processing and network communication.

### 🔒 Privacy

The core speech-to-text pipeline can run locally:

```text
Microphone
    ↓
Local AI Inference
    ↓
Transcript
    ↓
Caption
```

No cloud speech API is required for the offline pipeline.

### 🌐 Offline Capability

The application is designed to work in both connected and disconnected environments.

---

# 🛠️ Technical Implementation

## 🎤 Speech-to-Text

LiveLine supports two inference paths:

### CPU Backend

The CPU backend uses Whisper locally and is useful for development, testing, and UI integration.

### Snapdragon NPU Backend

The NPU backend is designed around Qualcomm AI Hub's precompiled QNN-compatible Whisper models.

The intended inference pipeline is:

```text
Whisper Model
      ↓
QNN / ONNX
      ↓
ONNX Runtime
      ↓
QNN Execution Provider
      ↓
Snapdragon NPU
```

---

## 🌍 Translation

Translation is an optional stage in the LiveLine pipeline.

```text
Speech
  ↓
Whisper
  ↓
Transcript
  ↓
Optional Translation
  ↓
Translated Caption
```

Keeping translation optional allows the core captioning pipeline to remain lightweight.

Future versions can expand support for additional Indian languages.

---

# 📁 Project Structure

```text
liveline/
│
├── engine.py
│   ├── CPUWhisperEngine
│   └── QNNWhisperEngine
│
├── live_demo.py
│   └── Console live-captioning loop
│
├── overlay.py
│   └── Always-on-top caption overlay
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Setup

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/liveline.git
cd liveline
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🧪 Run It Today — CPU Version

You can test LiveLine without Snapdragon-specific setup.

```bash
python live_demo.py --backend cpu --chunk 4
```

Speak into your microphone.

LiveLine will:

1. Capture microphone audio
2. Process audio in chunks
3. Generate speech-to-text
4. Display timestamped captions
5. Save the transcript

The transcript is written to:

```text
transcript.txt
```

This CPU path allows development and UI testing before configuring the Snapdragon NPU environment.

---

# 💻 Snapdragon Setup

## 1. Check Your Snapdragon Chipset

Open Windows PowerShell:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name
```

Note the exact processor name.

The precompiled Qualcomm AI Hub model binaries are chipset-specific, so make sure the selected model supports your target Snapdragon platform.

---

## 2. Install the Whisper Model Package

For Whisper Tiny:

```bash
pip install "qai_hub_models[whisper_tiny_en]"
```

Configure Qualcomm AI Hub if required:

```bash
qai-hub configure --api_token YOUR_TOKEN
```

Get an API token from:

https://aihub.qualcomm.com

---

## 3. Verify the Installed API

Qualcomm AI Hub model APIs may vary between releases.

Check the installed `App` interface:

```bash
python -c "from qai_hub_models.models.whisper_tiny_en import App; help(App)"
```

If the installed API differs from the implementation in `engine.py`, update the `QNNWhisperEngine` integration accordingly.

---

# ⚡ Run the NPU Version

After configuring the required QNN environment:

```bash
python live_demo.py --backend qnn --chunk 4
```

The NPU backend uses the same engine interface as the CPU backend.

---

# 🖥️ Caption Overlay

Run the caption overlay using CPU:

```bash
python overlay.py --backend cpu --chunk 4
```

Once the NPU backend is configured:

```bash
python overlay.py --backend qnn --chunk 4
```

The UI does not need to change when switching between inference backends.

---

# 📊 Benchmarking

LiveLine includes a CPU vs NPU latency comparison workflow.

### CPU

```bash
python live_demo.py --backend cpu --chunk 4
```

### NPU

```bash
python live_demo.py --backend qnn --chunk 4
```

The application reports the measured latency for each backend.

Example:

```text
Backend: CPU
Average latency: XX ms

Backend: Snapdragon NPU
Average latency: YY ms
```

> ⚠️ Actual latency depends on the Snapdragon chipset, Whisper model, quantization, audio chunk size, runtime version, thermal conditions, and system configuration. Benchmark results should be measured on the actual target HP Snapdragon PC.

---

# 🔒 Privacy

LiveLine is designed around an **on-device processing architecture**.

```text
             ┌─────────────────┐
             │   Microphone    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Local Inference │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    Transcript   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Caption Overlay │
             └─────────────────┘
```

The offline pipeline does not require sending microphone audio to a cloud speech API.

---

# ✈️ Offline Demo

LiveLine can be demonstrated with network connectivity disabled.

### Demo flow

```text
1. Start LiveLine
       ↓
2. Disable Wi-Fi / enable Airplane Mode
       ↓
3. Speak into microphone
       ↓
4. Whisper processes audio locally
       ↓
5. Captions appear on screen
       ↓
6. Transcript is saved locally
```

This demonstrates the offline-first design of the application.

---

# 🎯 Demo & Impact

The LiveLine demo focuses on a realistic meeting or classroom environment.

### Demonstration

The demo showcases:

* 🎤 Live microphone input
* 📝 Real-time captions
* ✈️ Offline operation
* ⚡ NPU vs CPU latency
* 🌍 Optional translation
* 🖥️ Caption overlay
* 📄 Local transcript export

### Intended Impact

LiveLine explores how on-device AI can make captioning more accessible in situations where cloud connectivity is unavailable or undesirable.

Potential use cases include:

* Accessibility support
* Classrooms
* Meetings
* Interviews
* Field work
* Travel
* Low-connectivity regions

---

# 🗺️ Roadmap

* [ ] Additional Indian language support
* [ ] Improved on-device translation
* [ ] Speaker identification
* [ ] Better caption styling and customization
* [ ] Sign-language recognition as a complementary accessibility feature
* [ ] Snapdragon handset/mobile version
* [ ] More Snapdragon chipset optimization
* [ ] Extended NPU benchmarking

---

# 🔮 Future Vision

LiveLine aims to demonstrate a broader idea:

> **AI does not always need the cloud.**

With capable NPUs available on modern devices, applications such as speech recognition, translation, and accessibility tools can increasingly move closer to the user.

LiveLine explores this approach through an offline-first captioning experience.

---

# 🏆 Built For

**Snapdragon® AI Lab Build & Present Challenge**

Powered by Qualcomm AI technologies.

---

# 📜 License

Add your preferred open-source license here.

For example:

```text
MIT License
```

---

# 👨‍💻 Project

**LiveLine**
On-Device Live Captioning & Translation

Built with:

* Python
* Whisper
* ONNX Runtime
* Qualcomm AI Hub
* QNN
* Snapdragon NPU
* Tkinter
