p = [["P1",0,5], ["P2",1,3], ["P3",2,6]]
q = 2

r = [5,3,6]
ct = [0,0,0]
queue = []
t = 0
done = 0

while done < 3:
    for i in range(3):
        if p[i][1] <= t and r[i] > 0 and i not in queue:
            queue.append(i)

    if not queue:
        t += 1
        continue

    i = queue.pop(0)
    x = min(q, r[i])
    t += x
    r[i] -= x

    for j in range(3):
        if p[j][1] <= t and r[j] > 0 and j not in queue and j != i:
            queue.append(j)

    if r[i] > 0:
        queue.append(i)
    else:
        ct[i] = t
        done += 1

tat = [ct[i] - p[i][1] for i in range(3)]
wt = [tat[i] - p[i][2] for i in range(3)]

print("Average Turnaround Time:", sum(tat)/3)
print("Average Waiting Time:", sum(wt)/3)
