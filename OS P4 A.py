processes = [
    {"pid": 1, "at": 0, "bt": 5},
    {"pid": 2, "at": 1, "bt": 3},
    {"pid": 3, "at": 2, "bt": 8},
    {"pid": 4, "at": 3, "bt": 6},
]

processes.sort(key=lambda p: p["at"])

time = 0
total_wt = 0
total_tat = 0
gantt = []

for p in processes:
    if time < p["at"]:
        time = p["at"]      

    gantt.append(f"P{p['pid']}")

    time += p["bt"]
    p["ct"] = time
    p["tat"] = p["ct"] - p["at"]
    p["wt"] = p["tat"] - p["bt"]

    total_wt += p["wt"]
    total_tat += p["tat"]

print("\n--- Gantt Chart ---")
print("| " + " | ".join(gantt) + " |")

print("\nPID\tAT\tBT\tCT\tTAT\tWT")
for p in processes:
    print(f"P{p['pid']}\t{p['at']}\t{p['bt']}\t{p['ct']}\t{p['tat']}\t{p['wt']}")

n = len(processes)
print(f"\nAverage Waiting Time = {total_wt/n:.2f}")
print(f"Average Turnaround Time = {total_tat/n:.2f}")
print("S120 ABHAY YADAV")
