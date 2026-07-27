processes = [
    {"pid": 1, "at": 0, "bt": 7, "done": False},
    {"pid": 2, "at": 2, "bt": 4, "done": False},
    {"pid": 3, "at": 4, "bt": 1, "done": False},
    {"pid": 4, "at": 5, "bt": 4, "done": False},
]
n = len(processes)
completed = 0
time = 0
total_wt = 0
total_tat = 0
gantt = []
while completed < n:
    idx = -1
    min_bt = float('inf')

    for i, p in enumerate(processes):
        if p["at"] <= time and not p["done"]:
            if p["bt"] < min_bt:
                min_bt = p["bt"]
                idx = i

    if idx == -1:
        time += 1  
        continue
    p = processes[idx]
    gantt.append(f"P{p['pid']}")

    time += p["bt"]
    p["ct"] = time
    p["tat"] = p["ct"] - p["at"]
    p["wt"] = p["tat"] - p["bt"]
    p["done"] = True

    total_wt += p["wt"]
    total_tat += p["tat"]
    completed += 1
print("\n--- Gantt Chart ---")
print("| " + " | ".join(gantt) + " |")
print("\nPID\tAT\tBT\tCT\tTAT\tWT")
for p in processes:
    print(f"P{p['pid']}\t{p['at']}\t{p['bt']}\t{p['ct']}\t{p['tat']}\t{p['wt']}")

print(f"\nAverage Waiting Time = {total_wt/n:.2f}")
print(f"Average Turnaround Time = {total_tat/n:.2f}")
print("S120 ABHAY YADAV")

