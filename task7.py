"""Q7 - Contact-Merging Program (designed from requirements)"""
import random, re, time

TITLES = {"dr", "mr", "mrs", "ms", "prof", "sri", "shri"}

def norm_number(raw):
    """Keep digits only; drop country code / leading 0 -> last 10 digits. '' if unusable."""
    d = re.sub(r"\D", "", raw or "")
    if len(d) < 10:
        return ""
    return d[-10:]

def norm_name(raw):
    words = re.sub(r"[^a-z\s]", " ", (raw or "").lower()).split()
    return " ".join(w for w in words if w not in TITLES)

def norm_email(raw):
    return (raw or "").strip().lower()

def merge(contacts):
    """Hash-based merge. Contacts that share a normalised number or e-mail are one person."""
    parent = list(range(len(contacts)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    seen = {}                                     # normalised number/e-mail -> first contact index
    for i, c in enumerate(contacts):
        keys = [("n", norm_number(n)) for n in c.get("numbers", []) if norm_number(n)]
        keys += [("e", norm_email(e)) for e in c.get("emails", []) if norm_email(e)]
        for k in keys:
            if k in seen:
                parent[find(i)] = find(seen[k])
            else:
                seen[k] = i
    groups = {}
    for i, c in enumerate(contacts):
        g = groups.setdefault(find(i), {"names": set(), "numbers": set(), "emails": set()})
        if c.get("name"):
            g["names"].add(c["name"].strip())
        g["numbers"].update(norm_number(n) for n in c.get("numbers", []) if norm_number(n))
        g["emails"].update(norm_email(e) for e in c.get("emails", []) if norm_email(e))
    result = []
    for g in groups.values():
        name = max(g["names"], key=lambda s: (len(norm_name(s)), s)) if g["names"] else "(no name)"
        result.append({"name": name, "numbers": sorted(g["numbers"]), "emails": sorted(g["emails"])})
    return sorted(result, key=lambda r: norm_name(r["name"]))

def merge_pairwise(contacts):
    """Compare every pair -> O(n^2)."""
    sig = []
    for c in contacts:
        s = {("n", norm_number(n)) for n in c.get("numbers", []) if norm_number(n)}
        s |= {("e", norm_email(e)) for e in c.get("emails", []) if norm_email(e)}
        sig.append(s)
    parent = list(range(len(contacts)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in range(len(contacts)):
        for j in range(i + 1, len(contacts)):
            if sig[i] & sig[j]:
                parent[find(i)] = find(j)
    return len({find(i) for i in range(len(contacts))})

if __name__ == "__main__":
    print("=== Normalisation tests ===")
    for x in ["+91 98400 12345", "9840012345", "098400-12345", "044 2345 6789", "12345"]:
        print(f"  {x!r:<20} -> {norm_number(x)!r}")
    for x in ["Dr. Ravi", "ravi kumar", "  MRS. Lakshmi  S ", "R@vi"]:
        print(f"  {x!r:<22} -> {norm_name(x)!r}")

    print("\n=== Small case merged by hand ===")
    small = [
        {"name": "Dr. Ravi", "numbers": ["+91 98400 12345"], "emails": []},
        {"name": "ravi kumar", "numbers": ["9840012345", "98410 55555"], "emails": ["Ravi@Mail.com"]},
        {"name": "Ravi K", "numbers": ["984105 5555"], "emails": []},
        {"name": "Anitha", "numbers": ["90000 11111"], "emails": []},
        {"name": "Anitha", "numbers": ["80000 22222"], "emails": []},     # same name, different person
        {"name": "Meena", "numbers": [], "emails": ["meena@x.org"]},       # missing number
        {"name": "Meena S", "numbers": [], "emails": ["MEENA@x.org"]},
        {"name": "", "numbers": ["70000 33333"], "emails": []},            # missing name
    ]
    print("Input contacts:", len(small))
    out = merge(small)
    for r in out:
        print(" ", r)
    print("Merged contacts:", len(out), "(expected 5: Ravi, Anitha, Anitha, Meena, no-name)")

    print("\n=== Timing ===")
    random.seed(11)
    first = ["ravi", "anitha", "kumar", "meena", "suresh", "divya", "arun", "priya", "karthik", "lakshmi"]
    def make(n):
        people = []
        for p in range(max(1, int(n * 0.7))):
            people.append({"num": f"9{random.randint(10**8, 10**9-1)}", "num2": f"8{random.randint(10**8, 10**9-1)}",
                           "name": random.choice(first) + " " + random.choice(first)})
        cs = []
        for _ in range(n):
            p = random.choice(people)
            fmt = random.choice(["+91 {}", "{}", "0{}", "+91-{}"])
            cs.append({"name": random.choice(["Dr. ", "", "Mr. "]) + p["name"], "numbers": [fmt.format(p["num"])], "emails": []})
        return cs
    print(f"{'contacts':>9} {'dictionary merge (s)':>21} {'pairwise (s)':>14} {'unique people':>14}")
    for n in (1000, 100000):
        cs = make(n)
        s = time.perf_counter(); r = merge(cs); td = time.perf_counter() - s
        if n <= 1000:
            s = time.perf_counter(); k = merge_pairwise(cs); tp = time.perf_counter() - s
            tps = f"{tp:.4f}"
            assert k == len(r)
        else:
            sub = cs[:3000]
            s = time.perf_counter(); merge_pairwise(sub); tp = (time.perf_counter() - s) * (n / 3000) ** 2
            tps = f"~{tp:.0f}*"
        print(f"{n:>9} {td:>21.4f} {tps:>14} {len(r):>14}")
    print("(* estimated from n=3000 scaled by (n/3000)^2, because it is O(n^2))")