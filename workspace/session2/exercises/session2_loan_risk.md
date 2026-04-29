# Session 2: Loan Portfolio Risk Analysis

## Overview

You have a loan portfolio, state banking regulations, and an internal risk policy. Use Claude Code to read all three sources, combine the rules, and produce a risk report.

## Data

The folder `data/loan-risk-analysis/` contains:

- **loan_tape.xlsx** — 220 loans: Borrower ID, Loan Amount, Interest Rate, Term, FICO Score, LTV Ratio, DTI Ratio, Delinquency Status, Property State, Loan Purpose, Origination Date
- **state_regulations.pdf** — Regulatory thresholds for 6 states (LTV caps, FICO thresholds, DTI limits), embedded in narrative text
- **risk_policy.docx** — Internal 4-tier risk classification system with special conditions

## Tasks

Ask Claude Code to:

(a) Extract the state-specific regulatory thresholds from the PDF
(b) Extract the risk tier classification criteria from the Word doc
(c) Assign each loan a risk tier and flag state-specific regulatory violations
(d) Produce a risk report showing tier distribution, flagged loans, and total estimated reserves

## What to Watch For

- The regulatory rules are embedded in dense narrative text (not tables) — does Claude extract them correctly?
- The internal policy has overlapping criteria and "any" vs "all" logic — does Claude apply them correctly?
- Special conditions (concentration risk, vintage risk, rate risk) can override normal tiering

## Deliverables

- Risk report spreadsheet with tier assignments, flags, and reserves
