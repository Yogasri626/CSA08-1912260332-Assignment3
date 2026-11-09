"""Q1 alternative: deque(maxlen=7) window and dictionary keyed by date"""
from collections import deque
from datetime import date, timedelta
import random
random.seed(1)
vals = [round(random.uniform(0, 20), 1) for _ in range(10)]
start = date(2025, 1, 1)
rain = {start + timedelta(days=i): v for i, v in enumerate(vals)}   # dict keyed by date
window, out = deque(maxlen=7), []
for d in sorted(rain):
    window.append(rain[d])                  # oldest value drops out automatically
    if len(window) == 7:
        out.append((d.isoformat(), round(sum(window) / 7, 2)))   # sum of 7 -> O(7n) overall
print("dict size:", len(rain), "| deque length:", len(window))
print("7-day averages (date, avg):", out)
rain[date(2025, 1, 4)] = 3.3                # late reading: O(1) assignment by date, no shifting
print("late reading stored in O(1):", rain[date(2025, 1, 4)])