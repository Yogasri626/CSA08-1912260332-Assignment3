"""Q3 - Dictionaries: Farmer Helpline Complaint Analysis"""
import random, re, string, time
from collections import Counter

print("=== Complete the Code (TODO 1 and TODO 2) ===")
calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}

def frequencies(texts, stop):
    # TODO 1: word -> count for every word not in stop, using dict.get()
    counts = {}
    for text in texts:
        for w in text.split():
            if w not in stop:
                counts[w] = counts.get(w, 0) + 1
    return counts

def top(counts, k):
    # TODO 2: k most frequent (word, count) pairs, highest first, ties alphabetical
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]

print(top(frequencies(calls, STOP), 3))

def clean_words(text, stop=frozenset()):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return [w for w in text.split() if w not in stop]

def freq_dict(words):
    d = {}
    for w in words:
        d[w] = d.get(w, 0) + 1
    return d

def freq_setdefault(words):
    d = {}
    for w in words:
        d.setdefault(w, [0])[0] += 1
    return {k: v[0] for k, v in d.items()}

def freq_listcount(words):
    return {w: words.count(w) for w in set(words)}

print("\n=== get() vs setdefault() ===")
w = "seeds price seeds subsidy price seeds".split()
print("get()       :", freq_dict(w))
print("setdefault():", freq_setdefault(w))

print("\n=== Group complaints by district / crop (dict of lists) ===")
records = [
    ("Madurai", "paddy", "seeds not received"),
    ("Salem", "cotton", "fertiliser price high"),
    ("Madurai", "cotton", "pump subsidy delayed"),
    ("Erode", "paddy", "seeds delayed"),
    ("Salem", "paddy", "seeds price high"),
]
by_district, by_crop = {}, {}
for dist, crop, text in records:
    by_district.setdefault(dist, []).append(text)
    by_crop.setdefault(crop, []).append(text)
for d, lst in by_district.items():
    print(f"{d:<8} {len(lst)} complaint(s): {lst}")
print("by crop:", {k: len(v) for k, v in by_crop.items()})

print("\n=== Views: keys(), values(), items() ===")
d = {"seeds": 3, "price": 2}
kv, vv, iv = d.keys(), d.values(), d.items()
print(kv, vv, iv)
d["subsidy"] = 1
print("after adding a key (views are live):", kv, vv)

print("\n=== Edge cases: empty text, case, punctuation ===")
print("empty text          :", top(frequencies([""], STOP), 3))
print("empty list          :", top(frequencies([], STOP), 3))
msg = ["Seeds NOT received!", "SEEDS, price... High?"]
print("raw split (no clean):", freq_dict([x for m in msg for x in m.split()]))
print("cleaned             :", freq_dict([x for m in msg for x in clean_words(m, STOP)]))

print("\n=== Timing: dict vs list.count() vs Counter ===")
vocab = ["seeds", "price", "subsidy", "rain", "pump", "loan", "urea", "paddy", "cotton", "pest"] + [f"w{i}" for i in range(190)]
random.seed(1)
def make(n):
    return [" ".join(random.choice(vocab) for _ in range(6)) for _ in range(n)]
print(f"{'complaints':>11} {'words':>8} {'dict':>9} {'list.count':>11} {'Counter':>9}")
for n in (1000, 10000, 100000):
    texts = make(n)
    words = [x for t in texts for x in t.split()]
    s = time.perf_counter(); a = freq_dict(words); t1 = time.perf_counter() - s
    if n <= 10000:
        s = time.perf_counter(); b = freq_listcount(words); t2 = time.perf_counter() - s
        t2s = f"{t2:.4f}"
        assert a == b
    else:
        # measured on 10% of the data and scaled (list.count is O(n*d))
        sub = words[: len(words) // 10]
        s = time.perf_counter(); freq_listcount(sub); t2 = (time.perf_counter() - s) * 10
        t2s = f"~{t2:.2f}*"
    s = time.perf_counter(); c = Counter(words); t3 = time.perf_counter() - s
    assert a == dict(c)
    print(f"{n:>11} {len(words):>8} {t1:>9.4f} {t2s:>11} {t3:>9.4f}")
print("(* estimated from 10% of the data, because it is O(n*d))")