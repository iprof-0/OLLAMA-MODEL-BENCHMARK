# OLLAMA Model Benchmark – Prof-0

A lightweight benchmarking tool for testing **OLLAMA local LLM models** performance in terms of **Read TPS**, **Write TPS**, and execution stability.

Designed for developers, researchers, and security engineers who want **real metrics**, not vibes.

> _"No System is secure."_ – Prof-0

---

## 📌 What This Script Does

This script benchmarks multiple OLLAMA models by:
- Sending the **same prompt** to each model
- Running multiple iterations per model
- Measuring:
  - **Prompt Read Tokens Per Second**
  - **Generation Write Tokens Per Second**
- Averaging results for fair comparison

It helps you decide:
- Which model is faster on your machine
- Which model is stable
- Which model is too heavy for your hardware

---

## 🧠 How It Works (High Level)

For each model:
1. A fixed prompt is sent to the OLLAMA `/generate` API
2. OLLAMA returns:
   - Prompt token count & duration
   - Generation token count & duration
3. TPS is calculated using nanosecond precision
4. Results are averaged across multiple runs

No streaming. No tricks. Raw engine numbers.

---

## ⚙️ Requirements

### System
- Local OLLAMA server running
- Python **3.9+**
- Enough RAM for the selected models

### Python Dependencies
```bash
pip install requests
