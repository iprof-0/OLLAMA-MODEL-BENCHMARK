# [OLLAMA](https://ollama.com/) Model Benchmark – [Prof-0](https://iprof-0.github.io/Zero)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Backend-OLLAMA-orange?style=for-the-badge)

A lightweight and accurate benchmarking tool for testing **OLLAMA local LLM models** performance in terms of:

- **Read TPS** (Prompt Tokens Per Second)
- **Write TPS** (Generation Tokens Per Second)
- **Execution stability**

Built for developers, researchers, and security engineers who care about **engine-level metrics**, not marketing numbers.

> _"No System is secure."_ – Prof-0

---

## 📌 Features

- **Minimal Dependencies**  
  Uses only `requests`. No bloat.

- **Warmup Phase**  
  Runs a configurable warmup cycle to load models into RAM/VRAM before benchmarking, avoiding cold-start bias.

- **High-Precision Metrics**  
  Uses nanosecond timing directly from OLLAMA engine responses.

- **Multiple Iterations & Averaging**  
  Repeats runs per model to reduce noise and outliers.

- **Graceful Failure Handling**  
  Timeouts, crashes, or invalid responses are handled without stopping the benchmark.

- **Clean Terminal Output**  
  Colored, readable, and suitable for screenshots or logs.

---

## 🧠 How It Works

For each model:

1. **Warmup Run (Optional)**  
   Sends a single prompt to load the model into memory.

2. **Benchmark Runs**
   - Sends a fixed prompt
   - Collects:
     - `prompt_eval_count`
     - `prompt_eval_duration`
     - `eval_count`
     - `eval_duration`

3. **TPS Calculation**
   - Read TPS = `prompt_eval_count / prompt_eval_duration`
   - Write TPS = `eval_count / eval_duration`

4. **Averaging**
   - Results are averaged across iterations for stability.

All measurements are performed locally using OLLAMA’s `/generate` API.

---

## ⚙️ Requirements

### System
- [OLLAMA](https://ollama.com/download) installed and running
- If you’re new, search [“How to install Ollama”](https://www.google.com/search?q=how%20to%20install%20ollama) for a guided walkthrough
- Local models already pulled
- [Python](https://www.python.org/downloads/) **3.9+**

### Python Dependency
```bash
pip install requests
```

---

## 🚀 Quick Start

### 1. Start OLLAMA
Make sure OLLAMA is running on:
```
http://localhost:11434
```

---

### 2. Configure Models

Edit [main.py](main.py) and add your installed models:

```python
TARGET_MODELS = [
    "phi3:mini",
    "qwen2.5:1.5b",
    # Add your models here
]
```

---

### 3. Tune Benchmark Settings

```python
ITERATIONS = 3
WARMUP_RUNS = 1
TIMEOUT = 300
```

---

### 4. Run

```bash
python main.py
```

---

## 📊 Sample Output

```
================================================================
           OLLAMA MODEL BENCHMARK  |  Prof-0
================================================================

Configuration: 3 Iterations | 1 Warmup | Temp 0.0

Model                    |     Read TPS |    Write TPS
----------------------------------------------------------------
phi3:mini                |       145.20 |        62.40
qwen2.5:1.5b             |       210.55 |        85.10

================================================================
Benchmark completed.
```

---

## 🔐 Security Notes

- No data is stored
- No external network calls
- 100% local execution

---

## 🧑‍💻 [Author](https://iprof-0.github.io/Zero)

**Zero (Prof-0)**  
Ethical Cybersecurity Researcher  

> _No System is secure._

---

## 📜 [License](LICENSE)

MIT License  
Copyright (c) 2026 [Zero](https://iprof-0.github.io/Zero/#contact)
