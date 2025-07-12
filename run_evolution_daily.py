import time
import auto_evolve

while True:
    print("🧬 Running daily evolution check...")
    auto_evolve.auto_evolve()
    print("✅ Evolution cycle complete.\n\n")
    time.sleep(86400)  # Wait one day before next run