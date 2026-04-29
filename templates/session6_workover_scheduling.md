# Exercise 5: Workover Rig Scheduling

## The Problem

You manage workover operations for a West Texas oil field. Twenty wells need maintenance, and you have three rigs available. Each well loses production every day it waits — some lose $21,700/day, others $3,150/day. Your goal: schedule the rigs to minimize total production loss.

This is hard to solve by intuition. There are an enormous number of possible schedules (20 wells assigned to 3 rigs, each with a different sequence). Greedy rules like "go to the biggest loss first" or "go to the nearest well" give decent but suboptimal answers because they ignore the interaction between travel time, service duration, and loss rate.

## Your Task

1. **Open the data file:** `data/workover_rig_data.md` — it contains well locations, service durations, daily production losses, travel time formulas, and all assumptions.

2. **Paste the data into Claude** (or ask Claude to read it) and describe the goal:
   > Find the schedule that minimizes total production loss across all 20 wells using 3 rigs.

3. **Pay attention to:**
   - Does Claude explain its approach?
   - Does the proposed schedule look reasonable? (High-loss wells served early? Nearby wells grouped on the same rig?)
   - What total production loss does it report (in barrels and dollars)?

4. **Challenge the result:**
   - Ask: "What if Rig C breaks down — re-optimize with 2 rigs."
   - Ask: "What if we prioritize wells in the eastern half of the field first?"

## Verification

After you have a proposed schedule, verify it:

> Generate 10,000 random feasible schedules by randomly assigning the 20 wells to 3 rigs and randomly ordering each rig's sequence. For each random schedule, compute the total production loss. Then:
> 1. Show a histogram of the 10,000 random total losses
> 2. Mark where your proposed schedule falls on the histogram
> 3. Report the best random schedule, the worst, the average, and how your proposal compares

If the AI's solution beats 9,900+ out of 10,000 random schedules, that's strong evidence it found a good answer — even though we can't prove it's globally optimal.
