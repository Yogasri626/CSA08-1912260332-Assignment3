"""Q5 - List Comprehension: Cleaning Sensor Readings"""
import random, sys, time

def loop_version(readings):
    celsius, fahrenheit, alarms = [], [], []
    for c in readings:
        if -50 <= c <= 50:
            celsius.append(c)
            fahrenheit.append(c * 9 / 5 + 32)
    for minute, c in enumerate(readings):
        if -50 <= c <= 50 and not (2 <= c <= 8):
            alarms.append(minute)
    return celsius, fahrenheit, alarms

def comp_version(readings):
    celsius = [c for c in readings if -50 <= c <= 50]
    fahrenheit = [c * 9 / 5 + 32 for c in readings if -50 <= c <= 50]
    alarms = [m for m, c in enumerate(readings) if -50 <= c <= 50 and not (2 <= c <= 8)]
    return celsius, fahrenheit, alarms

def map_version(readings):
    celsius = list(filter(lambda c: -50 <= c <= 50, readings))
    fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))
    alarms = [m for m, c in filter(lambda p: -50 <= p[1] <= 50 and not (2 <= p[1] <= 8), enumerate(readings))]
    return celsius, fahrenheit, alarms

sample = [4.5, 7.9, 9.2, -999, 1.0, 6.0, 120, 3.3, -50.0, 8.0]
print("Sample readings:", sample)
for name, f in (("for loop", loop_version), ("comprehension", comp_version), ("map/filter", map_version)):
    c, fh, al = f(sample)
    print(f"\n[{name}]")
    print(" valid Celsius   :", c)
    print(" Fahrenheit      :", [round(x, 1) for x in fh])
    print(" alarm minutes   :", al)

print("\n=== Dictionary and set comprehension ===")
print("dict {minute: F} for valid:", {m: round(c * 9 / 5 + 32, 1) for m, c in enumerate(sample) if -50 <= c <= 50})
print("set of distinct whole-degree valid readings:", {int(c) for c in sample if -50 <= c <= 50})

print("\n=== Verify the three versions give identical results ===")
random.seed(7)
big = [round(random.uniform(-60, 60), 1) for _ in range(100000)]
r1, r2, r3 = loop_version(big), comp_version(big), map_version(big)
print("loop == comprehension:", r1 == r2)
print("loop == map/filter   :", r1 == r3)

print("\n=== Edge cases ===")
allvalid = [5.0] * 10
allinvalid = [100, -100, 999] * 3
print("all valid  : celsius", len(comp_version(allvalid)[0]), "alarms", len(comp_version(allvalid)[2]))
print("all invalid: celsius", len(comp_version(allinvalid)[0]), "alarms", len(comp_version(allinvalid)[2]))
print("empty      :", comp_version([]))

print("\n=== Timing (seconds, best of 3) ===")
print(f"{'n':>9} {'for loop':>10} {'comprehension':>14} {'map/filter':>11}")
for n in (10_000, 100_000, 1_000_000):
    data = [round(random.uniform(-60, 60), 1) for _ in range(n)]
    res = []
    for f in (loop_version, comp_version, map_version):
        best = 9e9
        for _ in range(3):
            s = time.perf_counter(); f(data); best = min(best, time.perf_counter() - s)
        res.append(best)
    print(f"{n:>9} {res[0]:>10.4f} {res[1]:>14.4f} {res[2]:>11.4f}")

print("\n=== Memory: list comprehension vs generator (1,000,000 readings) ===")
lc = [c for c in data if -50 <= c <= 50]
ge = (c for c in data if -50 <= c <= 50)
print("list comprehension :", sys.getsizeof(lc), "bytes")
print("generator expression:", sys.getsizeof(ge), "bytes")
s = time.perf_counter(); a = sum([c for c in data if -50 <= c <= 50]); t1 = time.perf_counter() - s
s = time.perf_counter(); b = sum(c for c in data if -50 <= c <= 50); t2 = time.perf_counter() - s
print(f"sum via list: {a:.1f} in {t1:.4f}s | sum via generator: {b:.1f} in {t2:.4f}s")