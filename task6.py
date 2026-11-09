"""Q6 - Nested Data: A Railway Timetable"""
import random, sys, time

timetable = {
    "12601": {"name": "Chennai - Mumbai Express",
              "route": [("Chennai Central", "-", "06:00"), ("Arakkonam", "06:55", "06:57"),
                        ("Katpadi", "08:05", "08:10"), ("Mumbai CST", "22:30", "-")],
              "days": {"Mon", "Wed", "Fri"}},
    "12622": {"name": "Tamil Nadu Express",
              "route": [("Chennai Central", "-", "22:00"), ("Katpadi", "23:55", "00:00"),
                        ("Vijayawada", "04:30", "04:40"), ("New Delhi", "07:10", "-")],
              "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
    "12007": {"name": "Shatabdi Express",
              "route": [("Chennai Central", "-", "06:00"), ("Katpadi", "07:35", "07:37"),
                        ("Bengaluru", "11:00", "-")],
              "days": {"Tue", "Thu", "Sat"}},
    "16051": {"name": "Katpadi Passenger",
              "route": [("Katpadi", "-", "05:30"), ("Arakkonam", "07:10", "07:12"),
                        ("Chennai Central", "08:30", "-")],
              "days": {"Mon", "Tue", "Wed", "Thu", "Fri"}},
    "22637": {"name": "West Coast Express",
              "route": [("Chennai Central", "-", "13:10"), ("Katpadi", "15:20", "15:25"),
                        ("Mangaluru", "06:00", "-")],
              "days": {"Sun", "Fri"}},
}

def print_timetable(tt):
    for no, t in tt.items():
        print(f"\nTrain {no} - {t['name']}  (runs: {', '.join(sorted(t['days']))})")
        print(f"  {'Station':<18}{'Arr':>7}{'Dep':>7}")
        for st, arr, dep in t["route"]:
            print(f"  {st:<18}{arr:>7}{dep:>7}")

def departure_from(t, station):
    for st, arr, dep in t["route"]:
        if st == station:
            return dep
    return None

def trains_at(tt, station, day):
    """Without index: scan every train and every stop -> O(total stops)."""
    out = []
    for no, t in tt.items():
        if day in t["days"] and any(st == station for st, _, _ in t["route"]):
            out.append(no)
    return out

def build_index(tt):
    idx = {}
    for no, t in tt.items():
        for st, _, _ in t["route"]:
            idx.setdefault(st, []).append(no)
    return idx

def trains_at_indexed(tt, idx, station, day):
    return [no for no in idx.get(station, []) if day in tt[no]["days"]]

def sort_by_departure(tt, trains, station):
    key = lambda no: departure_from(tt[no], station) if departure_from(tt[no], station) not in (None, "-") else "99:99"
    return sorted(trains, key=lambda no: key(no))

if __name__ == "__main__":
    print_timetable(timetable)

    print("\n=== Access expression ===")
    print("timetable['12601']['route'][2][2] ->", timetable["12601"]["route"][2][2], "(departure at the third station)")

    print("\n=== Query: trains stopping at Katpadi on Fri, sorted by departure ===")
    found = trains_at(timetable, "Katpadi", "Fri")
    for no in sort_by_departure(timetable, found, "Katpadi"):
        print(f"  {no}  {timetable[no]['name']:<26} departs Katpadi {departure_from(timetable[no], 'Katpadi')}")

    print("\n=== Edge cases ===")
    print("unknown station 'Atlantis' :", trains_at(timetable, "Atlantis", "Fri"))
    print("train not running that day (Shatabdi 12007 on Fri):", "12007" in trains_at(timetable, "Chennai Central", "Fri"))
    idx = build_index(timetable)
    print("index agrees with scan :", sorted(trains_at(timetable, "Katpadi", "Fri")) == sorted(trains_at_indexed(timetable, idx, "Katpadi", "Fri")))

    print("\n=== Timing: station queries with and without index ===")
    stations = [f"S{i}" for i in range(500)]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    random.seed(3)
    print(f"{'trains':>7} {'stops':>8} {'scan (ms/query)':>16} {'index (ms/query)':>17} {'index build (ms)':>17} {'index mem (KB)':>15}")
    for n in (100, 1000, 10000):
        tt = {}
        for i in range(n):
            route = [(s, "00:00", "00:05") for s in random.sample(stations, 12)]
            tt[str(i)] = {"name": f"T{i}", "route": route, "days": set(random.sample(days, 4))}
        total = sum(len(t["route"]) for t in tt.values())
        q = [random.choice(stations) for _ in range(50)]
        s = time.perf_counter()
        for st in q: trains_at(tt, st, "Mon")
        t_scan = (time.perf_counter() - s) / 50 * 1000
        s = time.perf_counter(); idx = build_index(tt); t_build = (time.perf_counter() - s) * 1000
        s = time.perf_counter()
        for st in q: trains_at_indexed(tt, idx, st, "Mon")
        t_idx = (time.perf_counter() - s) / 50 * 1000
        mem = sys.getsizeof(idx) + sum(sys.getsizeof(v) for v in idx.values())
        print(f"{n:>7} {total:>8} {t_scan:>16.4f} {t_idx:>17.5f} {t_build:>17.2f} {mem/1024:>15.1f}")