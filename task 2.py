"""Q2 - Tuples, Mutability and Copying: City Bus-Stop Map"""
import copy, sys, time

print("=== Complete the Code (TODO 1) ===")
rows, cols = 3, 4
bad = [[0] * cols] * rows          # every row is the SAME list object
bad[0][1] = 7
# TODO 1: Create a rows x cols grid of zeros using a list comprehension
good = [[0 for _ in range(cols)] for _ in range(rows)]
good[0][1] = 7
print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])

print("\n=== Unpacking tuples in a for loop ===")
for (lat, lon), name in stops.items():
    print(f"{name:<16} lat={lat}  lon={lon}")

print("\n=== List as dictionary key ===")
try:
    stops[[13.0418, 80.2341]] = "Bad"
except TypeError as e:
    print("TypeError:", e)

print("\n=== Bug shown with is and id() ===")
print("bad :", [id(r) for r in bad], " all same:", bad[0] is bad[1] is bad[2])
print("good:", [id(r) for r in good], " all same:", good[0] is good[1] is good[2])

print("\n=== Aliasing, shallow copy, deep copy ===")
orig = [[1, 2], [3, 4]]
alias = orig
sh1 = copy.copy(orig)
sh2 = orig[:]
deep = copy.deepcopy(orig)
orig[0][0] = 99        # change an inner list
orig.append([5, 6])    # change the outer list
print("orig :", orig)
print("alias:", alias, " (same object:", alias is orig, ")")
print("copy.copy  :", sh1, " inner shared:", sh1[0] is orig[0])
print("slice [:]  :", sh2, " inner shared:", sh2[0] is orig[0])
print("deepcopy   :", deep, " inner shared:", deep[0] is orig[0])

print("\n=== Function changes caller's list ===")
def add_stop(lst):
    lst.append("New Stop")
mine = ["A", "B"]
add_stop(mine)
print("after add_stop:", mine)

print("\n=== Memory: list vs tuple of 1,000,000 values ===")
N = 1_000_000
L = list(range(N)); T = tuple(range(N))
print("sys.getsizeof(list) :", sys.getsizeof(L), "bytes")
print("sys.getsizeof(tuple):", sys.getsizeof(T), "bytes")
print("difference          :", sys.getsizeof(L) - sys.getsizeof(T), "bytes")

print("\n=== Timing: create and index (best of 5) ===")
def best(f, n=5):
    r = []
    for _ in range(n):
        s = time.perf_counter(); f(); r.append(time.perf_counter() - s)
    return min(r)
tc_list = best(lambda: list(range(N))); tc_tup = best(lambda: tuple(range(N)))
def idx(c):
    def g():
        for i in range(0, N, 1):
            c[i]
    return g
ti_list = best(idx(L), 3); ti_tup = best(idx(T), 3)
print(f"create list : {tc_list:.5f} s   create tuple: {tc_tup:.5f} s")
print(f"index list  : {ti_list:.5f} s   index tuple : {ti_tup:.5f} s (1,000,000 reads)")

print("\n=== List inside a tuple ===")
t = ([1, 2], 3)
t[0].append(99)
print("after t[0].append(99):", t)
try:
    t[0] = [0]
except TypeError as e:
    print("TypeError:", e)
try:
    t[0] += [5]
except TypeError as e:
    print("TypeError on t[0] += [5]:", e, "-> but t is now", t)