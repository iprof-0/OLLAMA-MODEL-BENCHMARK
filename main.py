import requests
import time
from statistics import mean
import sys

# =========================
# Config
# =========================
OLLAMA_HOST = "http://localhost:11434/api/generate"

TARGET_MODELS = [
    "phi3:mini",       # Example: lightweight
    "qwen2.5:1.5b",    # Example: fast
    # Add your models here
]

TEST_PROMPT = "Why is cybersecurity important? Answer in 50 words."
ITERATIONS = 3
WARMUP_RUNS = 1      # New: Run once to load model into VRAM
TIMEOUT = 300

# =========================
# Colors
# =========================
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
BOLD = "\033[1m"

# =========================
# Core Logic
# =========================
def get_engine_metrics(model: str, is_warmup: bool = False) -> dict:
    payload = {
        "model": model,
        "prompt": TEST_PROMPT,
        "stream": False,
        "options": {"temperature": 0.0} # Deterministic for benchmarking
    }

    try:
        start = time.time()
        res = requests.post(OLLAMA_HOST, json=payload, timeout=TIMEOUT)
        end = time.time()

        if res.status_code != 200:
            return {"success": False, "error": f"HTTP {res.status_code}"}

        data = res.json()

        # OLLAMA returns nanoseconds, convert to seconds
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

    except KeyboardInterrupt:
        print(f"\n{RED}[!] Benchmark interrupted by user.{RESET}")
        sys.exit(0)
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_benchmark():
    print(f"{CYAN}{'='*64}{RESET}")
    print(f"{BOLD}{CYAN}{'OLLAMA MODEL BENCHMARK  |  Prof-0':^64}{RESET}")
    print(f"{CYAN}{'='*64}{RESET}\n")
    print(f"{DIM}Configuration: {ITERATIONS} Iterations | {WARMUP_RUNS} Warmup | Temp 0.0{RESET}\n")

    header = f"{'Model':<24} | {'Read TPS':>12} | {'Write TPS':>12}"
    print(header)
    print("-" * len(header))

    for model in TARGET_MODELS:
        read_scores, write_scores = [], []
        
        # 1. Warmup Phase
        if WARMUP_RUNS > 0:
            print(f"{DIM}→ Warming up {model}...{RESET}", end="\r")
            get_engine_metrics(model, is_warmup=True)

        # 2. Testing Phase
        print(f"{YELLOW}→ Testing {model}...   {RESET}", end="\r")
        
        failed = False
        for _ in range(ITERATIONS):
            r = get_engine_metrics(model)
            if r["success"]:
                read_scores.append(r["read"])
                write_scores.append(r["write"])
            else:
                failed = True
                break
        
        # Clear the "Testing..." line
        print(f"{' '*40}", end="\r")

        if not failed and read_scores:
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
    print(f"{BOLD}Benchmark completed.{RESET}")

if __name__ == "__main__":
    run_benchmark()
