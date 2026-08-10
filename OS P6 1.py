processes = [
    ["P1", 0, 5],
    ["P2", 4, 2],
    ["P3", 5, 4]
]

quantum = 2


#  ROUND ROBIN
remaining = [p[2] for p in processes]
completion = [0, 0, 0]
queue = []
time = 0
done = 0

while done < 3:

    # Add arrived processes
    for i in range(3):
        if processes[i][1] <= time and remaining[i] > 0 and i not in queue:
            queue.append(i)

    if not queue:
        time += 1
        continue

    i = queue.pop(0)

    run = min(quantum, remaining[i])
    time += run
    remaining[i] -= run

    # Add newly arrived processes
    for j in range(3):
        if processes[j][1] <= time and remaining[j] > 0 and j not in queue and j != i:
            queue.append(j)

    if remaining[i] > 0:
        queue.append(i)
    else:
        completion[i] = time
        done += 1


tat = []
wt = []

for i in range(3):
    tat.append(completion[i] - processes[i][1])
    wt.append(tat[i] - processes[i][2])

print("ROUND ROBIN")
print("Average Turnaround Time:", sum(tat) / 3)
print("Average Waiting Time:", sum(wt) / 3)


#  FCFS 

time = 0
completion = []

for p in processes:

    if time < p[1]:
        time = p[1]

    time += p[2]
    completion.append(time)

tat = []
wt = []

for i in range(3):
    tat.append(completion[i] - processes[i][1])
    wt.append(tat[i] - processes[i][2])

print("\nFCFS")
print("Average Turnaround Time:", sum(tat) / 3)
print("Average Waiting Time:", sum(wt) / 3)
