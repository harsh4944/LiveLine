# 🎙️ LiveLine

### On-Device Live Captioning & Translation for Snapdragon-Powered HP PCs

**LiveLine** is an offline-first, privacy-preserving live captioning and translation assistant built for **Snapdragon-powered HP PCs**.

It transcribes speech in real time and optionally translates the transcript into another language — with inference designed to run **entirely on-device using the Snapdragon NPU**.

> Built for the **Snapdragon® AI Lab Build & Present Challenge by Qualcomm**

---

## ✨ Key Highlights

* 🎤 **Real-time speech-to-text**
* ⚡ **Snapdragon NPU acceleration**
* 🔒 **100% offline & privacy-first**
* 🌐 **Optional on-device translation**
* 🖥️ **Always-on-top caption overlay**
* 📄 **Continuous transcript export**
* ✈️ Works without an internet connection
* 📊 **NPU vs CPU latency benchmarking**

---

## 🧩 Problem

Modern real-time captioning and translation tools often depend on cloud-based speech APIs. This creates three major challenges:

### 🔐 Privacy

Meetings, interviews, classrooms, and other conversations may contain sensitive information. Sending audio to external servers introduces unnecessary privacy risks.

### 🌐 Internet Dependency

Cloud-based services stop working when connectivity is poor or unavailable. This is particularly challenging for:

* Rural classrooms
* Field teams
* Low-bandwidth environments
* Travel and offline environments

### ⏱️ Latency & Cost

Continuous cloud inference introduces network round trips and recurring per-minute processing costs.

---

## 💡 Solution

LiveLine brings speech recognition directly onto the user's PC.

### Offline-first

LiveLine is designed to work with **zero internet connectivity**.

### Privacy by design

Audio and inference remain on the local machine. There is no requirement to upload microphone data to a cloud speech API.

### Accessibility focused

LiveLine can assist:

* Hearing-impaired users
* Non-native speakers
* Students in classrooms
* Meeting participants
* Field workers
* Users operating in low-connectivity environments

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   Microphone     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Audio Chunks    │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Whisper STT Model   │
                 │   Snapdragon NPU     │
                 └───────────┬───────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Live Transcript  │
                    └────────┬─────────┘
                             │
                    Optional Translation
                             │
                             ▼
                 ┌────────────────────────┐
                 │ On-Device MT Model     │
                 └────────────┬───────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Caption Overlay  │
                    └──────────────────┘
```

---

## ⚙️ Technical Stack

| Component       | Technology                           |
| --------------- | ------------------------------------ |
| Speech-to-Text  | Whisper Tiny / Whisper Small         |
| AI Acceleration | Snapdragon NPU                       |
| Model Runtime   | ONNX Runtime                         |
| NPU Backend     | Qualcomm QNN Execution Provider      |
| Model Source    | Qualcomm AI Hub                      |
| Translation     | Optional on-device MT                |
| UI              | Python + Tkinter                     |
| Audio Input     | Microphone                           |
| Platform        | Windows on Snapdragon-powered HP PCs |

---

## 🚀 Why the Snapdragon NPU?

LiveLine is designed around local AI inference, making the Snapdragon NPU an important part of the architecture.

### ⚡ Low Latency

The Whisper encoder can achieve low inference latency on supported Snapdragon NPUs, helping keep captions close to real time.

### 🔋 Efficient Local AI

NPU acceleration allows AI workloads to run locally without continuously streaming audio to a remote service.

### 🔒 Privacy

The core pipeline can operate locally:

```text
Microphone
    ↓
Local AI inference
    ↓
Local transcript
    ↓
Caption
```

No cloud speech API is required.

### 🌐 Offline Capability

The same application can operate in connected and disconnected environments.

---

# 🛠️ Technical Implementation

## Speech-to-Text

LiveLine supports a CPU development path and a Snapdragon NPU path.

### CPU

The CPU backend uses Whisper for local speech recognition and is useful for development and UI testing.

### Snapdragon NPU

The NPU backend is designed around Qualcomm AI Hub's precompiled QNN-compatible Whisper models.

The intended execution path is:

```text
Whisper Model
     ↓
ONNX / QNN
     ↓
ONNX Runtime
     ↓
QNN Execution Provider
     ↓
Snapdragon NPU
```

---

## 🌍 Translation

Translation is an optional stage in the pipeline.

Keeping translation optional allows the core captioning pipeline to remain lightweight and responsive.

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
│   └── Console-based live captioning
│
├── overlay.py
│   └── Always-on-top caption UI
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

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

# 🧪 Run the CPU Version

You can test LiveLine without a Snapdragon-specific setup.

```bash
python live_demo.py --backend cpu --chunk 4
```

Speak into your microphone and LiveLine will generate timestamped captions.

A transcript is also written to:

```text
transcript.txt
```

This CPU path is useful for testing the application, microphone pipeline, UI, and overall user experience.

---

# 💻 Snapdragon NPU Setup

## 1. Check Your Snapdragon Chipset

On Windows PowerShell:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name
```

Record the exact processor name before selecting a Qualcomm AI Hub model.

---

## 2. Install Qualcomm AI Hub Model Package

For the Whisper Tiny model:

```bash
pip install "qai_hub_models[whisper_tiny_en]"
```

Configure your Qualcomm AI Hub credentials if required by the installed model workflow:

```bash
qai-hub configure --api_token YOUR_TOKEN
```

Qualcomm AI Hub:

https://aihub.qualcomm.com

---

## 3. Verify the Installed API

The Qualcomm AI Hub model APIs can change between releases.

Check the installed `App` interface before using the NPU backend:

```bash
python -c "from qai_hub_models.models.whisper_tiny_en import App; help(App)"
```

If the installed API differs from the implementation in `engine.py`, update the `QNNWhisperEngine` integration accordingly.

---

# ⚡ Run the NPU Version

Once the local QNN environment is configured:

```bash
python live_demo.py --backend qnn --chunk 4
```

LiveLine will use the QNN backend when the required model and runtime are available.

---

# 🖥️ Caption Overlay

Launch the graphical caption overlay:

```bash
python overlay.py --backend cpu --chunk 4
```

For the Snapdragon NPU backend:

```bash
python overlay.py --backend qnn --chunk 4
```

The same engine interface allows the UI to work with either backend.

---

# 📊 Benchmarking

LiveLine includes a CPU vs NPU benchmarking workflow.

Run the CPU version:

```bash
python live_demo.py --backend cpu --chunk 4
```

Then run the NPU version:

```bash
python live_demo.py --backend qnn --chunk 4
```

Compare the reported inference latency.

### Example

```text
Backend: CPU
Average latency: XX ms

Backend: Snapdragon NPU
Average latency: YY ms
```

> **Note:** Actual latency depends on the Snapdragon chipset, model variant, quantization, audio chunk size, runtime version, thermal conditions, and system configuration. Benchmark numbers should be reported from the target HP Snapdragon device rather than assumed values.

---

# 🔒 Privacy

LiveLine is designed around an **on-device processing architecture**.

```text
             ┌───────────────────────┐
             │       Microphone      │
             └───────────┬───────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │   Local
```
