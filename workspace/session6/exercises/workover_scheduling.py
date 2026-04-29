import math
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Well data
wells = [
    {"name":"W01","x":12,"y":8,"service":3,"loss":120},
    {"name":"W02","x":5,"y":22,"service":2,"loss":85},
    {"name":"W03","x":30,"y":15,"service":4,"loss":200},
    {"name":"W04","x":18,"y":3,"service":1,"loss":45},
    {"name":"W05","x":25,"y":28,"service":5,"loss":310},
    {"name":"W06","x":8,"y":14,"service":2,"loss":95},
    {"name":"W07","x":35,"y":7,"service":3,"loss":150},
    {"name":"W08","x":14,"y":30,"service":2,"loss":70},
    {"name":"W09","x":40,"y":20,"service":4,"loss":260},
    {"name":"W10","x":3,"y":10,"service":1,"loss":55},
    {"name":"W11","x":22,"y":18,"service":3,"loss":175},
    {"name":"W12","x":28,"y":5,"service":2,"loss":110},
    {"name":"W13","x":10,"y":25,"service":3,"loss":130},
    {"name":"W14","x":38,"y":12,"service":2,"loss":190},
    {"name":"W15","x":15,"y":20,"service":4,"loss":220},
    {"name":"W16","x":33,"y":25,"service":1,"loss":80},
    {"name":"W17","x":6,"y":5,"service":2,"loss":65},
    {"name":"W18","x":20,"y":32,"service":3,"loss":145},
    {"name":"W19","x":42,"y":28,"service":5,"loss":280},
    {"name":"W20","x":27,"y":14,"service":2,"loss":135},
]

def travel_time(x1, y1, x2, y2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    raw = dist / 240
    return math.ceil(raw * 2) / 2

def compute_total_loss(schedule):
    total_loss = 0
    for rig_wells in schedule:
        current_x, current_y = 0, 0
        current_time = 0
        for wi in rig_wells:
            w = wells[wi]
            tt = travel_time(current_x, current_y, w["x"], w["y"])
            arrival = current_time + tt
            completion = arrival + w["service"]
            total_loss += w["loss"] * completion
            current_time = completion
            current_x, current_y = w["x"], w["y"]
    return total_loss

def greedy_schedule():
    n_rigs = 3
    rig_time = [0.0] * n_rigs
    rig_pos = [(0, 0)] * n_rigs
    rig_schedule = [[] for _ in range(n_rigs)]
    assigned = set()

    for _ in range(len(wells)):
        best_cost = float('inf')
        best_rig = -1
        best_well = -1

        for wi in range(len(wells)):
            if wi in assigned:
                continue
            w = wells[wi]
            for ri in range(n_rigs):
                tt = travel_time(rig_pos[ri][0], rig_pos[ri][1], w["x"], w["y"])
                completion = rig_time[ri] + tt + w["service"]
                cost = w["loss"] * completion
                if cost < best_cost:
                    best_cost = cost
                    best_rig = ri
                    best_well = wi

        assigned.add(best_well)
        w = wells[best_well]
        tt = travel_time(rig_pos[best_rig][0], rig_pos[best_rig][1], w["x"], w["y"])
        rig_time[best_rig] += tt + w["service"]
        rig_pos[best_rig] = (w["x"], w["y"])
        rig_schedule[best_rig].append(best_well)

    return rig_schedule

def greedy_wspt():
    sorted_wells = sorted(range(len(wells)), key=lambda i: wells[i]["loss"]/wells[i]["service"], reverse=True)
    n_rigs = 3
    rig_time = [0.0] * n_rigs
    rig_pos = [(0, 0)] * n_rigs
    rig_schedule = [[] for _ in range(n_rigs)]

    for wi in sorted_wells:
        w = wells[wi]
        best_rig = -1
        best_completion = float('inf')
        for ri in range(n_rigs):
            tt = travel_time(rig_pos[ri][0], rig_pos[ri][1], w["x"], w["y"])
            completion = rig_time[ri] + tt + w["service"]
            if completion < best_completion:
                best_completion = completion
                best_rig = ri

        tt = travel_time(rig_pos[best_rig][0], rig_pos[best_rig][1], w["x"], w["y"])
        rig_time[best_rig] += tt + w["service"]
        rig_pos[best_rig] = (w["x"], w["y"])
        rig_schedule[best_rig].append(wi)

    return rig_schedule

def local_search(schedule, iterations=5000):
    best = [list(s) for s in schedule]
    best_cost = compute_total_loss(best)

    for _ in range(iterations):
        candidate = [list(s) for s in best]
        r = random.random()

        if r < 0.4:
            ri = random.randint(0, 2)
            if len(candidate[ri]) >= 2:
                i, j = random.sample(range(len(candidate[ri])), 2)
                candidate[ri][i], candidate[ri][j] = candidate[ri][j], candidate[ri][i]
        elif r < 0.7:
            from_rig = random.randint(0, 2)
            to_rig = random.randint(0, 2)
            if from_rig != to_rig and len(candidate[from_rig]) > 0:
                idx = random.randint(0, len(candidate[from_rig]) - 1)
                well = candidate[from_rig].pop(idx)
                ins = random.randint(0, len(candidate[to_rig]))
                candidate[to_rig].insert(ins, well)
        else:
            r1, r2 = random.sample(range(3), 2)
            if len(candidate[r1]) > 0 and len(candidate[r2]) > 0:
                i1 = random.randint(0, len(candidate[r1]) - 1)
                i2 = random.randint(0, len(candidate[r2]) - 1)
                candidate[r1][i1], candidate[r2][i2] = candidate[r2][i2], candidate[r1][i1]

        cost = compute_total_loss(candidate)
        if cost < best_cost:
            best = candidate
            best_cost = cost

    return best, best_cost

# Generate initial solutions
greedy1 = greedy_schedule()
greedy2 = greedy_wspt()

print("Greedy (incremental cost):", compute_total_loss(greedy1))
print("Greedy (WSPT):", compute_total_loss(greedy2))

# Local search from both
random.seed(42)
best_schedule = None
best_cost = float('inf')

for init in [greedy1, greedy2]:
    for _ in range(5):
        s, c = local_search(init, iterations=20000)
        if c < best_cost:
            best_cost = c
            best_schedule = s

print(f"\nBest after local search: {best_cost} bbl")
print(f"Best after local search: ${best_cost * 70:,.0f}")

# Print the schedule
for ri, rig_wells in enumerate(best_schedule):
    rig_name = ["A", "B", "C"][ri]
    print(f"\nRig {rig_name}:")
    current_x, current_y = 0, 0
    current_time = 0
    for wi in rig_wells:
        w = wells[wi]
        tt = travel_time(current_x, current_y, w["x"], w["y"])
        arrival = current_time + tt
        completion = arrival + w["service"]
        print(f"  {w['name']}: travel {tt}d, arrive day {arrival}, complete day {completion}, loss={w['loss']} bbl/day, total_loss={w['loss']*completion} bbl")
        current_time = completion
        current_x, current_y = w["x"], w["y"]

# Generate 10,000 random schedules
print("\n\nGenerating 10,000 random schedules...")
random.seed(123)
random_losses = []
for _ in range(10000):
    perm = list(range(20))
    random.shuffle(perm)
    cut1 = random.randint(1, 18)
    cut2 = random.randint(cut1+1, 19)
    sched = [perm[:cut1], perm[cut1:cut2], perm[cut2:]]
    random_losses.append(compute_total_loss(sched))

random_losses = np.array(random_losses)
print(f"Random: min={random_losses.min()}, max={random_losses.max()}, mean={random_losses.mean():.0f}, median={np.median(random_losses):.0f}")
print(f"Our solution: {best_cost}")
beats = np.sum(random_losses > best_cost)
print(f"Beats {beats} out of 10,000 random schedules ({beats/100:.1f}%)")

# Save histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(random_losses, bins=50, color='steelblue', alpha=0.7, edgecolor='white')
ax.axvline(best_cost, color='red', linewidth=2, linestyle='--', label=f'Our solution: {best_cost:,} bbl')
ax.axvline(random_losses.min(), color='green', linewidth=1.5, linestyle=':', label=f'Best random: {random_losses.min():,.0f} bbl')
ax.set_xlabel('Total Production Loss (barrels)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Workover Scheduling: 10,000 Random Schedules vs. Optimized Solution', fontsize=14)
ax.legend(fontsize=11)
ax.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.savefig('exercises/workover_scheduling_histogram.png', dpi=150)
print("\nHistogram saved to exercises/workover_scheduling_histogram.png")
