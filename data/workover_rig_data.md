# Workover Rig Scheduling Problem

## Background

You manage workover operations for a West Texas oil field. Twenty wells need workover service. You have three workover rigs available. Each well is losing production every day it waits for service, and each rig must travel between wells (travel time depends on distance). Your goal is to schedule the rigs to minimize total production loss.

**Total production loss** = for each well, (daily production loss) x (number of days from now until that well's workover is complete).

## Rigs

All three rigs are currently at the field yard (location: Row 0, Col 0 on the grid below). Each rig can service one well at a time. Once a rig finishes a well, it travels to the next well on its schedule.

| Rig | Starting Location | Daily Operating Cost |
|-----|-------------------|---------------------|
| Rig A | Field Yard (0, 0) | $15,000 |
| Rig B | Field Yard (0, 0) | $15,000 |
| Rig C | Field Yard (0, 0) | $15,000 |

## Wells Needing Service

Each well has a grid location (miles), an estimated service duration (days), and a daily production loss (barrels/day lost while waiting AND during service).

| Well | Location (x, y) | Service Duration (days) | Daily Production Loss (bbl/day) | Oil Price: $70/bbl |
|------|-----------------|------------------------|---------------------------------|---------------------|
| W01 | (12, 8) | 3 | 120 | $8,400/day |
| W02 | (5, 22) | 2 | 85 | $5,950/day |
| W03 | (30, 15) | 4 | 200 | $14,000/day |
| W04 | (18, 3) | 1 | 45 | $3,150/day |
| W05 | (25, 28) | 5 | 310 | $21,700/day |
| W06 | (8, 14) | 2 | 95 | $6,650/day |
| W07 | (35, 7) | 3 | 150 | $10,500/day |
| W08 | (14, 30) | 2 | 70 | $4,900/day |
| W09 | (40, 20) | 4 | 260 | $18,200/day |
| W10 | (3, 10) | 1 | 55 | $3,850/day |
| W11 | (22, 18) | 3 | 175 | $12,250/day |
| W12 | (28, 5) | 2 | 110 | $7,700/day |
| W13 | (10, 25) | 3 | 130 | $9,100/day |
| W14 | (38, 12) | 2 | 190 | $13,300/day |
| W15 | (15, 20) | 4 | 220 | $15,400/day |
| W16 | (33, 25) | 1 | 80 | $5,600/day |
| W17 | (6, 5) | 2 | 65 | $4,550/day |
| W18 | (20, 32) | 3 | 145 | $10,150/day |
| W19 | (42, 28) | 5 | 280 | $19,600/day |
| W20 | (27, 14) | 2 | 135 | $9,450/day |

## Travel Times

Travel time between any two locations = (straight-line distance) / 30 mph, rounded up to the nearest half day. Rigs travel on existing lease roads, but straight-line distance is a reasonable approximation.

**Formula:** Travel time (days) = ceiling( sqrt((x2-x1)^2 + (y2-y1)^2) / 30 / 8 * 2 ) / 2

That is, rigs drive 30 mph for 8 hours per day. Divide distance by 240 (miles per day), round up to nearest 0.5 day.

## Assumptions

- A well continues to lose production from Day 0 until the workover is **completed** (arrival + service duration).
- All 20 wells need service starting now (Day 0). There is no option to skip a well.
- Rigs work every day (no days off).
- A rig cannot start a new well until the current well is fully serviced.
- Rigs are identical in capability.

## Your Task

Determine which wells each rig should service and in what order, to **minimize the total production lost** (in barrels) across all 20 wells.

Report:
1. The schedule for each rig (sequence of wells with arrival and completion times)
2. The total production loss in barrels
3. The total production loss in dollars (at $70/bbl)

## Data in CSV Format

```csv
well,x,y,service_days,daily_loss_bbl
W01,12,8,3,120
W02,5,22,2,85
W03,30,15,4,200
W04,18,3,1,45
W05,25,28,5,310
W06,8,14,2,95
W07,35,7,3,150
W08,14,30,2,70
W09,40,20,4,260
W10,3,10,1,55
W11,22,18,3,175
W12,28,5,2,110
W13,10,25,3,130
W14,38,12,2,190
W15,15,20,4,220
W16,33,25,1,80
W17,6,5,2,65
W18,20,32,3,145
W19,42,28,5,280
W20,27,14,2,135
```
