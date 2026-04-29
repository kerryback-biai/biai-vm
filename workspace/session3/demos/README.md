# Session 3 Demos: Navigating Diverse Data Sources

All demos run on the XYZ Corp Custom Chatbot (separate platform, not AI Lab).

## Demo 1: Cross-System Fuzzy Merge
"Which of our customers buy from multiple divisions? Show combined revenue and flag any name mismatches across systems."
- Queries 3 CRMs (Salesforce, Legacy CRM, HubSpot)
- Resolves name mismatches (GE vs General Electric vs GE Safety Division)
- Expected: 10 customers in 2+ divisions, 4 in all 3 = $56.5M

## Demo 2: GroupBy Aggregate Across Systems
Revenue per employee by division — requires CRM + Workday join.

## Demo 3: Document Q&A with Citations
"What is our policy on remote work for the Energy Division?" — pulls from Employee Handbook with page citations.

## Demo 4: RAG Chunking Failure
"What are the termination penalties in our Apex Industries contract?" — demonstrates how chunking splits a critical clause across pages, causing a confident but incomplete answer that misses a $1.53M fee.

## Demo 5: Documents Plus Database
"What's our contractual commitment to GE, and how does their actual spending compare?" — combines contract terms (PDF) with CRM spending data.
