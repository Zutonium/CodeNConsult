# Grind & Crumb — Executive Intelligence & Turnaround Platform

An enterprise-grade executive dashboard and turnaround decision support system built for **Grind & Crumb**'s CEO (Anna Whitfield) and Executive Board.

The platform provides an end-to-end operational and financial diagnosis of the 12-store specialty café chain based on the complete FY 2025/26 dataset (£8.66M System Revenue, £1.07M Operating Profit).

---

## 🚀 Quick Start: How to Run the App

You have two convenient ways to run and view the app:

### Option 1: Instant Standalone in Any Browser (Zero Setup)
Simply open the self-contained `index.html` file in any web browser (Chrome, Edge, Firefox, Safari):
- Double-click `index.html` in Windows File Explorer, or
- Right-click `index.html` -> **Open with** -> **Google Chrome** (or Edge).

*The application contains all consolidated dataset metrics and executive models embedded directly inside, so all interactive charts, sliders, simulators, and CEO AI responses work out of the box with zero internet dependencies.*

### Option 2: Live Python Server (Full API, Data Upload & Gemini Proxying)
To enable live backend file uploads and direct Gemini API proxying, run the Python server:
```powershell
python server.py
```
Then navigate to:
```
http://localhost:8080
```

---

## 🌟 Key Dashboard Features & Requirements Covered

### 1. 🏬 Overall Stores View
- **Worst Profit / Loss Ranking:** Clearly highlights **Manchester Piccadilly (S07)** losing **-£49,697** (-4.5% margin) despite generating the highest revenue in the chain (£1.11M), followed by **Leeds Trinity (S12)** (+£25.0k / 5.0% margin), **Sheffield Uni Campus (S11)** (+£30.8k / 8.5% margin), and **Hull Paragon (S10)** (+£47.8k / 8.9% margin).
- **Store-by-Store Profit Generation:** Complete financial comparison table across all 12 stores with revenues, rent, labour, food waste, profit, and margins.
- **Profit Trajectory & Dips Graph:** Interactive 12-month multi-line chart (July 2025 – June 2026) showing Leeds Briggate's drop when Trinity opened in September 2025, the January oat milk surcharge drop, and April wage rise.
- **AI Store Classification:** Status badges categorize stores into **Performing Well**, **Middle Performing**, and **Underperforming / Drag**, with tailored operational explanations and root-cause diagnoses.

### 2. 📍 Store Deep Dive & Management
- Dedicated store picker for all 12 stores (S01 to S12).
- Complete P&L statement (Revenue by channel, COGS ingredients, Labour, Rent, Rates, Utilities, Repairs, Other Opex, Delivery commissions & packaging).
- Footfall door counts, seating capacity, conversion rate %, staff rota daypart hours, and customer complaint themes.
- Store-specific **AI Diagnostic Headline** and tailored **Turnaround Action Plan**.

### 3. 💸 Costs & Savings
- Granular breakdown of all cost categories:
  - **Labour:** £2,504,509 (28.9% of sales)
  - **Delivery of Ingredients (COGS):** £2,372,799 (27.4% of sales)
  - **Property Rent:** £1,473,750 (17.0% of sales)
  - **Delivery Commissions & Packaging:** £450k+
  - **Utilities:** £371,460
  - **Business Rates:** £324,228
  - **Consumables & Hygiene Opex:** £187,688
  - **Repairs & Maintenance:** £107,640
  - **Historical Capex:** £860,000 (S12 fitout £385k, S03 refit £210k, S01 refit £140k, S05 refit £125k)
- **AI Cost Levers:** Concrete renegotiation strategies (renegotiating Dashly 33% commission, stopping boiler emergency callouts at Hull, cleaning staff vs overtime).
- **Interactive Cost Savings Simulator:** Toggle individual cost-saving initiatives to project **+£123,640/year in net savings**, lifting chain margin from 12.3% to **13.7%**!

### 4. 📈 Income & Menu ROI
- Channel sales mix: **In-Store (£6.02M / 69.5%)**, **Delivery (£1.52M / 17.6%)**, **App Click & Collect (£1.12M / 12.9%)**.
- **Top 10 Best Sellers vs Bottom 10 Products** by revenue and volume.
- **Full Menu Items ROI Matrix:** Unit economics for all 38 products (Price, Unit Cost, Unit Margin, Margin %, Annual Qty, Gross Profit, and ROI %).
- **Major Event Impact Analysis:**
  - The £0.40 Oat Milk Surcharge backlash vs Bean Social free plant milk.
  - App v3.0 redesign bugs and customer loyalty friction.
  - Leeds Trinity cannibalizing Leeds Briggate.

### 5. 🛵 Delivery Hub & Pricing Calculator
- Partner share: **RushEats (62.4%, 30% commission)** vs **Dashly (37.6%, jumped to 33% commission on April 1, 2026)**.
- **The Under-£8 Problem:** 29.0% of all delivery orders are under £8 (solo £3.50 coffees) that lose money after commission, packaging, and barista time.
- **Interactive Delivery Pricing Calculator:** Adjust Minimum Basket Size, Small Order Fee, Commission Rate, and Menu Markup with real-time calculation of net margin per delivery order and annual chain profit boost (+£48k/yr).

### 6. 👥 Staff, Rota & Turnover
- Turnover ranking across stores: Piccadilly (220% turnover, 53 leavers, 4.96/10 survey score), Spinningfields (81% turnover), Hull (162% turnover).
- Exit survey root-causes: Workload/understaffing (#1) and pay (#2).
- Daypart rota hours (Morning, Lunch, Afternoon).
- **Interactive Shift & Lunch Rush Simulator:** Shift hours from morning/afternoon into the critical 11:30–13:30 lunch rush to reduce walkouts by 65% and capture +£58,400 in lost sales!

### 7. 🗑️ Waste Management
- Total annual waste cost: **£133,815**.
- Category breakdown:
  - **Lunch (Sandwiches/Salads):** £68,162 (8.8% waste rate) — highest cash loss!
  - **Bakery:** £52,367 (11.7% waste rate) — 52,652 units discarded!
  - **Breakfast:** £13,286 (6.7% waste rate).
- Highest wastage stores: Leeds Briggate (£16.6k), Hull Paragon (£16.3k), Manchester Piccadilly (£16.1k).
- Actionable AI solutions: Dynamic par-level AI, 3pm dynamic app markdowns, and Too Good To Go surplus bags.

### 8. 💼 Future Investments: The £1.5M Capital Budget Allocation
- Complete appraisal of candidate sites CS1 to CS7 against footfall, rent, fitout, EBITDA, and cannibalization risk.
- **Warning against the traps:**
  - **DO NOT OPEN Leeds Wellington Place (CS7):** High rent (£11.8k/mo), footfall only 9,500, extreme cannibalization of S03 and S12. Projected **loss of -£82,414/yr** with a 99-year payback!
  - **DO NOT OPEN Sheffield Kelham Island (CS2):** Fitout £390k on low footfall yields 25.3-year payback.
- **Recommended £1.5M Capital Division:**
  1. **CS3: Manchester Oxford Road** (£240,000) — 52k footfall, 1.2-yr payback (+£192k EBITDA/yr)
  2. **CS4: York Station Kiosk** (£180,000) — Proven transit kiosk model, 1.3-yr payback (+£135k EBITDA/yr)
  3. **CS1: Leeds Headingley** (£320,000) — Suburban student corridor, 2.4-yr payback (+£134k EBITDA/yr)
  4. **York Stonegate Refit (S04)** (£160,000) — Modernize chain's top earner (£192k profit)
  5. **Piccadilly Dispatch Hatch & Rota (S07)** (£90,000) — Unclog lunch counter bottleneck
  6. **Hull Paragon Boiler & Cleaner (S10)** (£50,000) — Replace broken boiler/dishwasher
  7. **Digital App v4.0 & Par AI** (£160,000) — Reward recovery & predictive waste reduction
  8. **Staff Retention Fund** (£100,000) — 50p/hr lunch premium for transit baristas
  9. **Contingency Reserve** (£200,000) — Working capital buffer
  - **Total: £1,500,000** generating **+£691,431/yr in incremental EBITDA** (2.17-year blended payback, +64.8% EBITDA growth!).
- **Interactive Capital Allocation Planner:** Test custom budget combinations in real time.

### 9. 🤖 CEO AI Chatbot (Gemini Powered)
- Conversational executive assistant for CEO Anna Whitfield and the Board.
- Pre-loaded with prompt chips:
  - *"Why is Manchester Piccadilly losing money?"*
  - *"Where should I allocate the £1.5M budget?"*
  - *"Should we open Leeds Wellington Place?"*
  - *"How do we reduce waste at Leeds Briggate?"*
  - *"Should we scrap the oat milk surcharge?"*
- Supports direct Google Gemini API integration or instant built-in executive knowledge engine.

### 10. 📤 Data Upload & Real-Time Recalculation
- Drag-and-drop CSV upload tool to import new daily sales, waste logs, or rotas.
- Automatically recomputes metrics and updates charts in real time.

---

## 📁 Key File Structure

- `index.html` — The complete standalone interactive executive dashboard.
- `server.py` — Lightweight Python HTTP server handling REST APIs, Gemini proxying, and file uploads.
- `build_full_dataset.py` — Preprocessing pipeline compiling raw CSVs into consolidated data.
- `grind_and_crumb_data/full_dashboard_data.json` — Precomputed structured dataset (112 KB).
- `test_ceo.py` — Executive reasoning and prompt response engine.
- `build_index_html.py` — Master HTML generator.
