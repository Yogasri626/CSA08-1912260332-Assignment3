"""Q4 - Sets: Elective Registration Clash Detection"""
import random, time

print("=== Complete the Code (TODO 1: operators) ===")
ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1
both = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)

print("clash :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither :", sorted(neither))

print("\n=== Same result using set methods ===")
both2 = ai_elective.intersection(iot_elective)
exactly_one2 = ai_elective.symmetric_difference(iot_elective)
neither2 = all_students.difference(ai_elective.union(iot_elective))
print("clash same      :", both == both2)
print("exactly one same:", exactly_one == exactly_one2)
print("neither same    :", neither == neither2)

print("\n=== Other operations ===")
print("union (registered in at least one):", sorted(ai_elective | iot_elective))
print("AI only :", sorted(ai_elective - iot_elective))
print("IoT only:", sorted(iot_elective - ai_elective))

print("\n=== Duplicate removal ===")
raw = ["192311001", "192311004", "192311001", "192311004", "192311007"]
print("list :", raw, "->", len(raw), "entries")
print("set  :", sorted(set(raw)), "->", len(set(raw)), "entries")

print("\n=== Sets and tuples/lists ===")
print("set of tuples :", {(1, 2), (3, 4)})
try:
    {[1, 2]}
except TypeError as e:
    print("set of lists  : TypeError:", e)

print("\n=== Edge cases ===")
e, a = set(), ai_elective
print("empty & AI :", e & a, "| empty | AI == AI:", (e | a) == a, "| AI - empty == AI:", (a - e) == a)
same = set(ai_elective)
print("identical: & =", len(a & same), "| ^ =", len(a ^ same), "| - =", len(a - same))

print("\n=== Membership timing: x in list vs x in set ===")
print(f"{'n':>9} {'list (us)':>12} {'set (us)':>10}")
for n in (10_000, 100_000, 1_000_000):
    data = [str(192300000 + i) for i in range(n)]
    s = set(data)
    target = data[-1]                       # worst case for the list
    t = time.perf_counter()
    for _ in range(20): target in data
    tl = (time.perf_counter() - t) / 20
    t = time.perf_counter()
    for _ in range(20000): target in s
    ts = (time.perf_counter() - t) / 20000
    print(f"{n:>9} {tl*1e6:>12.2f} {ts*1e6:>10.4f}")

print("\n=== Common students: nested loops vs & ===")
print(f"{'n each':>9} {'nested (s)':>11} {'& (s)':>9} {'common':>7}")
for n in (500, 2000, 4000):
    random.seed(5)
    A = random.sample(range(10 * n), n); B = random.sample(range(10 * n), n)
    t = time.perf_counter()
    c1 = [x for x in A for y in B if x == y]
    tn = time.perf_counter() - t
    t = time.perf_counter(); c2 = set(A) & set(B); ts = time.perf_counter() - t
    assert set(c1) == c2
    print(f"{n:>9} {tn:>11.4f} {ts:>9.6f} {len(c2):>7}")

print("\n=== Hand verification (small case) ===")
A, B, U = {1, 2, 3}, {2, 3, 4}, {1, 2, 3, 4, 5}
print("A={1,2,3} B={2,3,4} U={1..5}")
print("A&B =", A & B, "(expected {2,3})")
print("A^B =", A ^ B, "(expected {1,4})")
print("U-(A|B) =", U - (A | B), "(expected {5})")