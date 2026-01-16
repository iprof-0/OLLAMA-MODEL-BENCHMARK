import requests
import time
from statistics import mean

# =========================
# Config
# =========================
OLLAMA_HOST = "http://localhost:11434/api/generate"

TARGET_MODELS = [
  #replace with your model
    "llava-phi3",
    "qwen2.5:1.5b",
    
]

TEST_PROMPT = "Why is cybersecurity important? Answer in 50 words."
ITERATIONS = 3
TIMEOUT = 300

# =========================
# Colors (optional)
# =========================
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"

# =========================
# Core Logic
# =========================
def get_engine_metrics(model: str) -> dict:
    payload = {
        "model": model,
        "prompt": TEST_PROMPT,
        "stream": False,
        "options": {"temperature": 0.0}
    }

    try:
        start = time.time()
        res = requests.post(OLLAMA_HOST, json=payload, timeout=TIMEOUT)
        end = time.time()

        if res.status_code != 200:
            return {"success": False}

        data = res.json()

        pe_count = data.get("prompt_eval_count", 0)
        pe_time = max(data.get("prompt_eval_duration", 1), 1)

        e_count = data.get("eval_count", 0)
        e_time = max(data.get("eval_duration", 1), 1)

        read_tps = pe_count / (pe_time / 1_000_000_000)
        write_tps = e_count / (e_time / 1_000_000_000)

        return {
            "read": read_tps,
            "write": write_tps,
            "total": end - start,
            "success": True
        }

    except Exception:
        return {"success": False}


def run_benchmark():
    print(f"{CYAN}{'='*64}{RESET}")
    print(f"{CYAN}{'OLLAMA MODEL BENCHMARK  |  Prof-0':^64}{RESET}")
    print(f"{CYAN}{'='*64}{RESET}\n")

    header = f"{'Model':<24} | {'Read TPS':>12} | {'Write TPS':>12}"
    print(header)
    print("-" * len(header))

    for model in TARGET_MODELS:
        read_scores, write_scores = [], []

        print(f"{DIM}→ Testing {model}{RESET}")

        for _ in range(ITERATIONS):
            r = get_engine_metrics(model)
            if r["success"]:
                read_scores.append(r["read"])
                write_scores.append(r["write"])

        if read_scores:
            print(
                f"{model:<24} | "
                f"{GREEN}{mean(read_scores):>12.2f}{RESET} | "
                f"{GREEN}{mean(write_scores):>12.2f}{RESET}"
            )
        else:
            print(
                f"{model:<24} | "
                f"{RED}{'FAILED':>12}{RESET} | "
                f"{RED}{'FAILED':>12}{RESET}"
            )

    print(f"\n{CYAN}{'='*64}{RESET}")
    print("Benchmark completed.")


if __name__ == "__main__":
    run_benchmark()
