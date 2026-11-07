import json, os

def build_html():
    with open('grind_and_crumb_data/full_dashboard_data.json', 'r', encoding='utf-8') as f:
        data_json = f.read()

    # We embed the data_json into the HTML so it works 100% offline or online!
    html_content = f'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grind & Crumb — Executive Intelligence & Turnaround Platform</title>
  <!-- Chart.js from CDN with local canvas fallback -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f2937;
      --card-hover: #1e293b;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --emerald: #10b981;
      --rose: #ef4444;
      --amber: #f59e0b;
      --purple: #8b5cf6;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    .light {{
      --bg: #f3f4f6;
      --card-bg: #ffffff;
      --card-border: #e5e7eb;
      --card-hover: #f9fafb;
      --text-main: #111827;
      --text-muted: #6b7280;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --emerald: #059669;
      --rose: #dc2626;
      --amber: #d97706;
      --purple: #7c3aed;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font);
    }}

    body {{
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      transition: background-color 0.2s, color 0.2s;
    }}

    /* Header */
    header {{
      background: var(--card-bg);
      border-bottom: 1px solid var(--card-border);
      padding: 1rem 1.75rem;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .logo-area {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, #d97706, #b45309);
      width: 42px;
      height: 42px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.25rem;
      color: #fff;
      box-shadow: 0 4px 10px rgba(217, 119, 6, 0.35);
    }}

    .brand-title {{
      font-size: 1.2rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .brand-sub {{
      font-size: 0.78rem;
      color: var(--text-muted);
      font-weight: 400;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .btn {{
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      border: 1px solid transparent;
      transition: all 0.15s ease;
    }}

    .btn-primary {{
      background: var(--accent);
      color: #fff;
    }}

    .btn-primary:hover {{
      background: var(--accent-hover);
    }}

    .btn-secondary {{
      background: var(--card-bg);
      border-color: var(--card-border);
      color: var(--text-main);
    }}

    .btn-secondary:hover {{
      background: var(--card-hover);
    }}

    .btn-ai {{
      background: linear-gradient(135deg, #8b5cf6, #ec4899);
      color: white;
      box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }}

    .btn-ai:hover {{
      opacity: 0.92;
      transform: translateY(-1px);
    }}

    /* Navigation tabs */
    .nav-bar {{
      background: var(--card-bg);
      border-bottom: 1px solid var(--card-border);
      padding: 0 1.75rem;
      display: flex;
      gap: 0.5rem;
      overflow-x: auto;
      white-space: nowrap;
      scrollbar-width: none;
    }}

    .nav-bar::-webkit-scrollbar {{
      display: none;
    }}

    .nav-tab {{
      padding: 0.85rem 1rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      border-bottom: 2px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.45rem;
      text-decoration: none;
    }}

    .nav-tab:hover {{
      color: var(--text-main);
    }}

    .nav-tab.active {{
      color: var(--accent);
      border-bottom-color: var(--accent);
    }}

    /* Main Container */
    main {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.5rem 1.75rem 3rem 1.75rem;
      width: 100%;
      flex: 1;
    }}

    /* KPI Banner */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.1rem 1.25rem;
      position: relative;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--accent);
    }}

    .kpi-card.emerald::before {{ background: var(--emerald); }}
    .kpi-card.rose::before {{ background: var(--rose); }}
    .kpi-card.amber::before {{ background: var(--amber); }}
    .kpi-card.purple::before {{ background: var(--purple); }}

    .kpi-label {{
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
    }}

    .kpi-value {{
      font-size: 1.6rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.2;
    }}

    .kpi-sub {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 0.35rem;
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 700;
    }}

    .badge-emerald {{
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .badge-rose {{
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    .badge-amber {{
      background: rgba(245, 158, 11, 0.15);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .badge-blue {{
      background: rgba(59, 130, 246, 0.15);
      color: #3b82f6;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    .badge-purple {{
      background: rgba(139, 92, 246, 0.15);
      color: #8b5cf6;
      border: 1px solid rgba(139, 92, 246, 0.3);
    }}

    /* Card Panels */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.35rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.15rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--card-border);
    }}

    .card-title {{
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .card-subtitle {{
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }}

    /* Tab views */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
      animation: fadeIn 0.2s ease-in-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Grid Layouts */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }}

    @media (max-width: 768px) {{
      .grid-2, .grid-3 {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--card-border);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.85rem;
    }}

    th {{
      background: var(--card-hover);
      padding: 0.75rem 1rem;
      font-weight: 700;
      color: var(--text-muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--card-border);
    }}

    td {{
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--card-border);
      color: var(--text-main);
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover td {{
      background: var(--card-hover);
    }}

    .text-right {{ text-align: right; }}
    .text-center {{ text-align: center; }}
    .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .font-semibold {{ font-weight: 600; }}
    .text-emerald {{ color: var(--emerald); }}
    .text-rose {{ color: var(--rose); }}
    .text-amber {{ color: var(--amber); }}

    /* AI Insight Box */
    .ai-box {{
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(59, 130, 246, 0.06));
      border: 1px solid rgba(139, 92, 246, 0.25);
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
    }}

    .ai-box-header {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.75rem;
    }}

    .ai-badge {{
      background: linear-gradient(135deg, #8b5cf6, #6366f1);
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}

    .ai-box-title {{
      font-weight: 700;
      font-size: 0.95rem;
    }}

    .ai-box ul {{
      margin-left: 1.25rem;
      margin-top: 0.5rem;
      line-height: 1.6;
      font-size: 0.87rem;
      color: var(--text-main);
    }}

    .ai-box li {{
      margin-bottom: 0.4rem;
    }}

    /* Form Controls */
    select, input, textarea {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 0.55rem 0.85rem;
      border-radius: 8px;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.15s;
    }}

    select:focus, input:focus, textarea:focus {{
      border-color: var(--accent);
    }}

    .slider-group {{
      margin-bottom: 1.25rem;
    }}

    .slider-header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.4rem;
      font-size: 0.85rem;
      font-weight: 600;
    }}

    .slider-val {{
      color: var(--accent);
      font-weight: 700;
    }}

    input[type=range] {{
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background: var(--card-border);
      outline: none;
      -webkit-appearance: none;
    }}

    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent);
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }}

    /* Chat Drawer Modal */
    .chat-drawer {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 440px;
      height: 620px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      box-shadow: 0 12px 36px rgba(0,0,0,0.4);
      display: none;
      flex-direction: column;
      z-index: 100;
      overflow: hidden;
      animation: slideUp 0.25s ease-out;
    }}

    .chat-drawer.open {{
      display: flex;
    }}

    @keyframes slideUp {{
      from {{ transform: translateY(40px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    .chat-header {{
      padding: 1rem 1.25rem;
      background: linear-gradient(135deg, #8b5cf6, #3b82f6);
      color: white;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .chat-body {{
      flex: 1;
      padding: 1rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }}

    .chat-msg {{
      max-width: 85%;
      padding: 0.75rem 0.95rem;
      border-radius: 12px;
      font-size: 0.85rem;
      line-height: 1.45;
    }}

    .chat-msg.bot {{
      background: var(--card-hover);
      border: 1px solid var(--card-border);
      align-self: flex-start;
      border-bottom-left-radius: 2px;
    }}

    .chat-msg.user {{
      background: var(--accent);
      color: white;
      align-self: flex-end;
      border-bottom-right-radius: 2px;
    }}

    .chat-footer {{
      padding: 0.85rem 1rem;
      border-top: 1px solid var(--card-border);
      display: flex;
      gap: 0.5rem;
      background: var(--card-bg);
    }}

    .prompt-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin-bottom: 0.6rem;
    }}

    .prompt-chip {{
      background: var(--card-hover);
      border: 1px solid var(--card-border);
      padding: 0.3rem 0.6rem;
      border-radius: 16px;
      font-size: 0.74rem;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s;
    }}

    .prompt-chip:hover {{
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }}

    /* Drop Zone */
    .dropzone {{
      border: 2px dashed var(--card-border);
      border-radius: 12px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      cursor: pointer;
      transition: border-color 0.2s;
    }}

    .dropzone:hover {{
      border-color: var(--accent);
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="logo-area">
      <div class="logo-badge">G&C</div>
      <div>
        <div class="brand-title">
          GRIND & CRUMB
          <span class="badge badge-purple" style="font-size:0.7rem;">CEO INTELLIGENCE PLATFORM</span>
        </div>
        <div class="brand-sub">12 Specialty Stores · Full FY 2025/26 Financials, Operations & Strategy</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn btn-secondary" onclick="toggleTheme()" id="themeBtn">☀️ Light</button>
      <button class="btn btn-ai" onclick="toggleChat()">🤖 CEO Chatbot</button>
    </div>
  </header>

  <!-- Navigation Bar -->
  <div class="nav-bar">
    <a class="nav-tab active" onclick="switchTab('overview')">🏬 Overall Stores View</a>
    <a class="nav-tab" onclick="switchTab('stores')">📍 Store Deep Dive</a>
    <a class="nav-tab" onclick="switchTab('costs')">💸 Costs & Savings</a>
    <a class="nav-tab" onclick="switchTab('income')">📈 Income & Menu ROI</a>
    <a class="nav-tab" onclick="switchTab('delivery')">🛵 Delivery Hub & Calculator</a>
    <a class="nav-tab" onclick="switchTab('staff')">👥 Staff, Rota & Turnover</a>
    <a class="nav-tab" onclick="switchTab('waste')">🗑️ Waste Management</a>
    <a class="nav-tab" onclick="switchTab('investments')">💼 Future Investments (£1.5M)</a>
    <a class="nav-tab" onclick="switchTab('upload')">📤 Upload New Data</a>
  </div>

  <!-- Main Content -->
  <main>

    <!-- Top Sticky Metric Ribbon -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Total System Revenue</div>
        <div class="kpi-value" id="kpi-revenue">£8,656,692</div>
        <div class="kpi-sub">
          <span class="badge badge-blue">12 Stores</span>
          <span>Full FY 25/26</span>
        </div>
      </div>

      <div class="kpi-card emerald">
        <div class="kpi-label">Chain Net Operating Profit</div>
        <div class="kpi-value text-emerald" id="kpi-profit">£1,065,766</div>
        <div class="kpi-sub">
          <span class="badge badge-emerald">12.31% Margin</span>
          <span>Operating EBITDA</span>
        </div>
      </div>

      <div class="kpi-card rose">
        <div class="kpi-label">Biggest Profit Drain (Most Loss)</div>
        <div class="kpi-value text-rose" id="kpi-worst-store">Manchester Picc.</div>
        <div class="kpi-sub">
          <span class="badge badge-rose">-£49,697 Loss</span>
          <span>£366k rent trap</span>
        </div>
      </div>

      <div class="kpi-card emerald">
        <div class="kpi-label">Top Profit Generator</div>
        <div class="kpi-value text-emerald" id="kpi-best-store">York Stonegate</div>
        <div class="kpi-sub">
          <span class="badge badge-emerald">£192,031</span>
          <span>21.6% margin</span>
        </div>
      </div>

      <div class="kpi-card amber">
        <div class="kpi-label">Chain Food Waste Lost</div>
        <div class="kpi-value text-amber" id="kpi-waste">£133,815</div>
        <div class="kpi-sub">
          <span class="badge badge-amber">11.7% Bakery</span>
          <span>8.8% Lunch waste</span>
        </div>
      </div>

      <div class="kpi-card purple">
        <div class="kpi-label">Small Delivery Leakage</div>
        <div class="kpi-value text-purple">29.0%</div>
        <div class="kpi-sub">
          <span class="badge badge-purple">&lt; £8 Orders</span>
          <span>Losing money on fees</span>
        </div>
      </div>
    </div>

    <!-- TAB 1: OVERALL STORES VIEW -->
    <div id="tab-overview" class="tab-content active">
      
      <!-- AI Executive Diagnostic Banner -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">Executive AI Briefing</span>
          <span class="ai-box-title">Grind & Crumb Portfolio Health & Root-Cause Diagnosis</span>
        </div>
        <p style="font-size:0.88rem; line-height:1.55; margin-bottom:0.6rem;">
          Grind & Crumb generated <strong>£8,656,692 in sales</strong> and <strong>£1,065,766 in profit</strong>. While revenue has grown annually, CEO Anna Whitfield noted profit has flatlined. Our diagnostic model reveals three critical drag-factors across the estate:
        </p>
        <ul>
          <li><strong>The Manchester Piccadilly (S07) £366k Rent Trap:</strong> Highest sales in the chain (£1.11M) but loses <strong>-£49,697</strong>. Rent of £30,500/month (33% of sales) combines with severe lunch delivery order bottlenecks that create 12-person queues and cause commuters to walk away to station concourse competitors. Barista turnover is catastrophic at 220%.</li>
          <li><strong>Leeds Cannibalization & Waste Shock:</strong> Opening Leeds Trinity (S12) in Sept 2025 cannibalized <strong>22% of Leeds Briggate's (S03) sales</strong>. Briggate’s store manager maintained legacy prep levels, making Briggate the highest food waste store in the chain (£16,649 lost).</li>
          <li><strong>Delivery Friction & Squeeze:</strong> 29% of delivery orders are under £8 (e.g. single coffees), generating negative profit after commission, packaging, and barista time. Dashly increased commission to 33% from April 1, squeezing margins further.</li>
        </ul>
      </div>

      <!-- Controls & Filter -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:0.75rem;">
        <div style="display:flex; gap:0.5rem; align-items:center;">
          <label style="font-size:0.85rem; font-weight:600; color:var(--text-muted);">Filter by Performance:</label>
          <select id="overview-filter" onchange="filterOverviewTable()">
            <option value="ALL">All Stores (12)</option>
            <option value="Performing Well">Performing Well (5)</option>
            <option value="Middle Performing">Middle Performing (4)</option>
            <option value="Underperforming">Underperforming / Drag (3)</option>
          </select>
        </div>
        <div style="font-size:0.82rem; color:var(--text-muted);">
          Click any store row to open its comprehensive operational deep dive.
        </div>
      </div>

      <!-- Store Comparison Table -->
      <div class="card" style="padding:0; overflow:hidden;">
        <div class="table-container" style="border:none;">
          <table id="overview-table">
            <thead>
              <tr>
                <th>Store</th>
                <th>Location / Format</th>
                <th class="text-right">Total Revenue</th>
                <th class="text-right">Rent (Annual)</th>
                <th class="text-right">Labour Cost</th>
                <th class="text-right">Food Waste</th>
                <th class="text-right">Net Profit / Loss</th>
                <th class="text-right">Margin %</th>
                <th class="text-center">Status</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody id="overview-tbody">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Charts Grid: Profit Ranking & Monthly Dips/Increases -->
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">📊 Annual Net Profit / Loss by Store</div>
              <div class="card-subtitle">Green denotes profitable stores; Red denotes loss-making stores</div>
            </div>
          </div>
          <div style="height:340px; position:relative;">
            <canvas id="profitRankChart"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">📈 Monthly Profit Trajectory & Dips</div>
              <div class="card-subtitle">Track Leeds Briggate dip after Trinity launch & Jan oat milk impact</div>
            </div>
            <div>
              <select id="chart-store-select" onchange="updateMonthlyProfitChart()">
                <option value="ALL">Top & Underperforming Stores</option>
                <option value="S07">S07 - Manchester Piccadilly (Loss Maker)</option>
                <option value="S03">S03 - Leeds Briggate (Cannibalized)</option>
                <option value="S12">S12 - Leeds Trinity (Ramping)</option>
                <option value="S04">S04 - York Stonegate (Top Earner)</option>
                <option value="S10">S10 - Hull Paragon (Aging Infrastructure)</option>
              </select>
            </div>
          </div>
          <div style="height:340px; position:relative;">
            <canvas id="monthlyTrendChart"></canvas>
          </div>
        </div>
      </div>

      <!-- AI Turnaround Levers for Underperforming Stores -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">💡 AI Turnaround Playbook: Getting Underperforming Stores to Profit</div>
            <div class="card-subtitle">Specific operational fixes derived from real chain data</div>
          </div>
        </div>
        <div class="grid-3">
          <div style="background:var(--card-hover); padding:1rem; border-radius:10px; border-left:4px solid var(--rose);">
            <div style="font-weight:700; font-size:0.92rem; margin-bottom:0.3rem;">1. Fix Manchester Piccadilly (S07)</div>
            <p style="font-size:0.8rem; line-height:1.45; color:var(--text-muted); margin-bottom:0.5rem;">
              Current loss: -£49.7k. Disconnect delivery riders from front counter with dedicated dispatch window (£90k capex). Add 2 peak lunch baristas to stop £65k in lost commuter walkouts, and renegotiate rent to a turnover model.
            </p>
            <span class="badge badge-emerald">+£115,000 / yr EBITDA Swing</span>
          </div>

          <div style="background:var(--card-hover); padding:1rem; border-radius:10px; border-left:4px solid var(--amber);">
            <div style="font-weight:700; font-size:0.92rem; margin-bottom:0.3rem;">2. Balance Leeds Market (S03 & S12)</div>
            <p style="font-size:0.8rem; line-height:1.45; color:var(--text-muted); margin-bottom:0.5rem;">
              Grace Okafor at Briggate must cut par prep by 20% to eliminate £6,000 of excess waste. Differentiate Trinity as grab-and-go student/office and Briggate as premium brunch experiential café.
            </p>
            <span class="badge badge-emerald">+£28,000 / yr Combined Gain</span>
          </div>

          <div style="background:var(--card-hover); padding:1rem; border-radius:10px; border-left:4px solid var(--blue);">
            <div style="font-weight:700; font-size:0.92rem; margin-bottom:0.3rem;">3. Hull Paragon (S10) Boiler & Cleanliness</div>
            <p style="font-size:0.8rem; line-height:1.45; color:var(--text-muted); margin-bottom:0.5rem;">
              Replace the broken boiler and commercial dishwasher (£15k capex) to eliminate £5k emergency engineer callouts. Rehire part-time cleaner to stop barista burnout and customer churn.
            </p>
            <span class="badge badge-emerald">+£18,000 / yr Net Impact</span>
          </div>
        </div>
      </div>

    </div>

    <!-- TAB 2: STORE DEEP DIVE -->
    <div id="tab-stores" class="tab-content">
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
          <div>
            <div class="card-title">📍 Store-by-Store Operational Management Deep Dive</div>
            <div class="card-subtitle">Select any of the 12 stores to inspect its complete financial statement, rent, rota, footfall, and tailored AI diagnosis.</div>
          </div>
          <div>
            <select id="store-selector" onchange="renderStoreDeepDive()" style="font-size:0.95rem; font-weight:700; padding:0.6rem 1rem;">
              <!-- Dynamic Options -->
            </select>
          </div>
        </div>
      </div>

      <!-- Store Headline Banner -->
      <div id="store-detail-banner" class="ai-box">
        <!-- Rendered via JS -->
      </div>

      <!-- Store Detailed Metrics Grid -->
      <div class="kpi-grid" id="store-kpi-grid">
        <!-- Rendered via JS -->
      </div>

      <div class="grid-2">
        <!-- Store P&L Breakdown Card -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">📄 Store Profit & Loss Breakdown (Annual)</div>
          </div>
          <table style="width:100%; font-size:0.85rem;" id="store-pnl-table">
            <!-- Dynamic rows -->
          </table>
        </div>

        <!-- Store Monthly Trend Chart -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">📈 12-Month Sales, Expenses & Profit</div>
          </div>
          <div style="height:320px; position:relative;">
            <canvas id="storeIndividualChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Rota & Footfall & Reviews for selected store -->
      <div class="grid-3">
        <div class="card">
          <div class="card-header"><div class="card-title">⏰ Weekly Rota Distribution</div></div>
          <div id="store-rota-summary"></div>
        </div>

        <div class="card">
          <div class="card-header"><div class="card-title">🚪 Footfall & Conversion</div></div>
          <div id="store-footfall-summary"></div>
        </div>

        <div class="card">
          <div class="card-header"><div class="card-title">💬 Customer Reviews & Feedback</div></div>
          <div id="store-reviews-summary"></div>
        </div>
      </div>
    </div>

    <!-- TAB 3: COSTS & SAVINGS -->
    <div id="tab-costs" class="tab-content">
      
      <!-- AI Suggestions on Costs -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">AI Cost Optimization Audit</span>
          <span class="ai-box-title">Where Money Can Be Saved, Renegotiated & Rethought</span>
        </div>
        <ul>
          <li><strong>Labour (£2,504,509 — 28.9% of sales):</strong> Do not cut aggregate labour; instead, <em>re-align hours</em>. Cut idle Monday/Tuesday morning shifts and redeploy 4-6 hours into the 11:30–13:30 rush at transit stores to stop commuter queue walkouts.</li>
          <li><strong>Delivery Commissions & Packaging (£450k+):</strong> Dashly raised commission from 27% to 33% (+6 percentage points!). Demand reversion to 28% under threat of exclusivity with RushEats (saves ~£22,000/yr).</li>
          <li><strong>Property Rent (£1,473,750):</strong> Piccadilly’s £366k rent is out of line with station footfall capture. Open landlord negotiations for a base + turnover clause.</li>
          <li><strong>Repairs & Maintenance (£108,000):</strong> Emergency callouts at Hull Paragon and Spinningfields for aging boilers/dishwashers are burning cash. Replace with modern capital assets.</li>
          <li><strong>Consumables & Hygiene (£188,000):</strong> Consolidate cleaning chemicals, cups, and paper consumables through a single national distributor to capture an estimated 8-10% bulk rebate (~£16,000).</li>
        </ul>
      </div>

      <!-- Granular Cost Cards -->
      <div class="grid-3" id="costs-cards-grid">
        <!-- Rendered via JS -->
      </div>

      <!-- Cost Breakdown Chart & Simulator -->
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">📊 Chainwide Cost Structure Breakdown</div>
          </div>
          <div style="height:320px; position:relative;">
            <canvas id="costDoughnutChart"></canvas>
          </div>
        </div>

        <!-- Interactive Cost Savings Simulator -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">🧮 Interactive Cost-Savings Simulator</div>
            <div class="card-subtitle">Toggle strategic levers to project annual chain savings</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.85rem;">
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" id="sim-dashly" onchange="runCostSim()" checked>
              <span>Renegotiate Dashly commission back to 28% from 33% <strong>(+£22,500/yr)</strong></span>
            </label>
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" id="sim-small-order" onchange="runCostSim()" checked>
              <span>Implement £8 delivery minimum / £1.50 small order fee <strong>(+£38,000/yr)</strong></span>
            </label>
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" id="sim-par-waste" onchange="runCostSim()" checked>
              <span>Dynamic AI Par-Level Forecasting (cuts 30% of waste) <strong>(+£40,140/yr)</strong></span>
            </label>
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" id="sim-boiler" onchange="runCostSim()" checked>
              <span>Hull boiler/equipment replacement (avoids callouts) <strong>(+£8,000/yr)</strong></span>
            </label>
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" id="sim-consumables" onchange="runCostSim()" checked>
              <span>Bulk chemical & packaging contract consolidation <strong>(+£15,000/yr)</strong></span>
            </label>

            <div style="margin-top:1rem; padding:1rem; background:var(--card-hover); border-radius:10px; border:1px solid var(--card-border);">
              <div style="font-size:0.85rem; color:var(--text-muted);">Total Projected Annual Cost Savings:</div>
              <div style="font-size:1.6rem; font-weight:800; color:var(--emerald);" id="sim-total-savings">£123,640 / year</div>
              <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.25rem;">Boosts chain net profit margin from 12.3% to <strong>13.7%</strong>!</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: INCOME & MENU ROI -->
    <div id="tab-income" class="tab-content">
      
      <!-- AI Menu Insights -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">AI Menu Engineering Insights</span>
          <span class="ai-box-title">Maximizing Revenue & Item Gross Margin</span>
        </div>
        <ul>
          <li><strong>Reverse the £0.40 Oat Milk Surcharge:</strong> Introduced in Jan 2026 to recover £40k, it generated 230+ furious reviews and drove customers to competitor Bean Social (who dropped plant milk charges). Scrap the surcharge immediately; customer churn outweighs the fee!</li>
          <li><strong>Push High-Margin Coffee & Cold Drinks:</strong> Americano (84.0% margin), Flat White (78.6%), and Iced Latte (77.4%) generate over 60% of total revenue. Prioritize these high-margin hero drinks at the till.</li>
          <li><strong>Promote Meal Deals to Lift Basket Size:</strong> Meal deals combine high-margin hot drinks with sandwiches, raising AOV while maintaining healthy 68% blended margin.</li>
        </ul>
      </div>

      <!-- Channel Revenue Grid -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">In-Store Sales</div>
          <div class="kpi-value">£6,016,099</div>
          <div class="kpi-sub"><span class="badge badge-blue">69.5% of total</span></div>
        </div>
        <div class="kpi-card emerald">
          <div class="kpi-label">Delivery Platform Sales</div>
          <div class="kpi-value text-emerald">£1,524,424</div>
          <div class="kpi-sub"><span class="badge badge-emerald">17.6% of total</span></div>
        </div>
        <div class="kpi-card purple">
          <div class="kpi-label">App Click & Collect</div>
          <div class="kpi-value text-purple">£1,116,169</div>
          <div class="kpi-sub"><span class="badge badge-purple">12.9% of total</span></div>
        </div>
      </div>

      <!-- Top and Bottom Products Table -->
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">🏆 Top 10 Best Selling Products (by Revenue)</div>
          </div>
          <div class="table-container">
            <table id="top-products-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Category</th>
                  <th class="text-right">Price</th>
                  <th class="text-right">Margin %</th>
                  <th class="text-right">Est Sales</th>
                </tr>
              </thead>
              <tbody id="top-products-tbody"></tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">⚠️ Bottom 10 Products (Low Sales / Lagging)</div>
          </div>
          <div class="table-container">
            <table id="bottom-products-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Category</th>
                  <th class="text-right">Price</th>
                  <th class="text-right">Margin %</th>
                  <th class="text-right">Est Sales</th>
                </tr>
              </thead>
              <tbody id="bottom-products-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Full Menu Items ROI Matrix -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">📊 Full Menu Items Economics & ROI Matrix</div>
            <div class="card-subtitle">38 Products ranked by Unit Margin & Estimated Annual ROI</div>
          </div>
        </div>
        <div class="table-container" style="max-height:420px; overflow-y:auto;">
          <table id="full-menu-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Product Name</th>
                <th>Category</th>
                <th class="text-right">Menu Price</th>
                <th class="text-right">Unit Cost</th>
                <th class="text-right">Unit Margin (£)</th>
                <th class="text-right">Gross Margin %</th>
                <th class="text-right">Est Annual Qty</th>
                <th class="text-right">Annual Gross Profit</th>
                <th class="text-right">ROI %</th>
              </tr>
            </thead>
            <tbody id="full-menu-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 5: DELIVERY HUB & PRICING CALCULATOR -->
    <div id="tab-delivery" class="tab-content">
      
      <!-- AI Delivery Guidance -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">AI Delivery Strategy</span>
          <span class="ai-box-title">Fixing the Delivery Margin Leakage</span>
        </div>
        <ul>
          <li><strong>The Under-£8 Problem:</strong> 29.0% of our delivery orders are under £8. When a customer orders a single £3.50 Americano on Dashly, commission takes £1.16, packaging costs £0.45, ingredients cost £0.56, and 4 minutes barista time costs £0.87. <strong>Net profit is £0.46 before overheads!</strong> Once station rent is factored in, these orders lose money while blocking physical queues.</li>
          <li><strong>Partner Strategy:</strong> RushEats generates 62.4% of delivery volume with a 30% commission rate. Dashly unilaterally raised commission to 33%. Follow RushEats’ recommendation to institute an <strong>£8 minimum basket or £1.50 small-order fee</strong>.</li>
        </ul>
      </div>

      <div class="grid-2">
        <!-- Delivery Breakdown Card -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">🛵 Delivery Order Basket Size Distribution</div>
          </div>
          <div style="height:280px; position:relative;">
            <canvas id="deliveryBasketChart"></canvas>
          </div>
          <div style="margin-top:1rem; display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div style="padding:0.75rem; background:var(--card-hover); border-radius:8px;">
              <div style="font-size:0.75rem; color:var(--text-muted);">RushEats Orders</div>
              <div style="font-size:1.2rem; font-weight:700;">6,976 (62.4%)</div>
              <div style="font-size:0.75rem; color:var(--emerald);">30.0% Commission</div>
            </div>
            <div style="padding:0.75rem; background:var(--card-hover); border-radius:8px;">
              <div style="font-size:0.75rem; color:var(--text-muted);">Dashly Orders</div>
              <div style="font-size:1.2rem; font-weight:700;">4,203 (37.6%)</div>
              <div style="font-size:0.75rem; color:var(--rose);">33.0% Commission (Jumped!)</div>
            </div>
          </div>
        </div>

        <!-- Interactive Delivery Pricing Calculator -->
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">🧮 Interactive Delivery Pricing & Margin Calculator</div>
              <div class="card-subtitle">Simulate pricing rules to protect delivery profit margins</div>
            </div>
          </div>

          <div class="slider-group">
            <div class="slider-header">
              <span>Minimum Basket Size Threshold (£)</span>
              <span class="slider-val" id="val-min-basket">£8.00</span>
            </div>
            <input type="range" id="slider-min-basket" min="0" max="15" step="0.5" value="8" oninput="calcDeliveryEconomics()">
          </div>

          <div class="slider-group">
            <div class="slider-header">
              <span>Small Order Surcharge (&lt; Minimum) (£)</span>
              <span class="slider-val" id="val-small-fee">£1.50</span>
            </div>
            <input type="range" id="slider-small-fee" min="0" max="3" step="0.25" value="1.50" oninput="calcDeliveryEconomics()">
          </div>

          <div class="slider-group">
            <div class="slider-header">
              <span>Delivery Partner Commission Rate (%)</span>
              <span class="slider-val" id="val-comm-rate">28.5%</span>
            </div>
            <input type="range" id="slider-comm-rate" min="20" max="35" step="0.5" value="28.5" oninput="calcDeliveryEconomics()">
          </div>

          <div class="slider-group">
            <div class="slider-header">
              <span>Menu Price Markup for Delivery (%)</span>
              <span class="slider-val" id="val-del-markup">10.0%</span>
            </div>
            <input type="range" id="slider-del-markup" min="0" max="30" step="1" value="10" oninput="calcDeliveryEconomics()">
          </div>

          <!-- Dynamic Output Card -->
          <div style="padding:1rem; background:var(--card-hover); border-radius:10px; border:1px solid var(--card-border); margin-top:1rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
              <span style="font-size:0.85rem; color:var(--text-muted);">Net Profit per Average Delivery Order:</span>
              <span style="font-weight:700; font-size:1rem;" id="calc-net-order-profit">£3.82</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
              <span style="font-size:0.85rem; color:var(--text-muted);">Delivery Operating Margin:</span>
              <span style="font-weight:700; font-size:1rem; color:var(--emerald);" id="calc-net-order-margin">27.4%</span>
            </div>
            <div style="border-top:1px solid var(--card-border); padding-top:0.6rem; display:flex; justify-content:space-between;">
              <span style="font-size:0.9rem; font-weight:700;">Projected Annual Chain Profit Uplift:</span>
              <span style="font-size:1.25rem; font-weight:800; color:var(--emerald);" id="calc-annual-delivery-uplift">+£48,200 / yr</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: STAFF, ROTA & TURNOVER -->
    <div id="tab-staff" class="tab-content">
      
      <!-- AI Staff Overview -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">AI Workforce Diagnostics</span>
          <span class="ai-box-title">Halting the Transit Churn & Lunch Rota Bottlenecks</span>
        </div>
        <ul>
          <li><strong>Catastrophic Turnover in Transit Hubs:</strong> Manchester Piccadilly has <strong>53 leavers on 24 headcount (220% turnover!)</strong> with an avg staff score of 4.96/10. Spinningfields had 39 new starters and 13 leavers (score 5.03/10). Baristas leave for concourse chains paying 50p/hr more because every lunch is a frantic "firefight".</li>
          <li><strong>Exit Survey Root Causes:</strong> Workload / understaffing during peak rushes (30 departures) and better pay elsewhere (26 departures) account for over 60% of all voluntary departures.</li>
          <li><strong>Operational Fix:</strong> Reallocate labour hours into the 11:30–13:30 peak and introduce a 50p/hr lunch rush retention premium in transit stores.</li>
        </ul>
      </div>

      <!-- Staff Metrics Grid -->
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">👥 Staff Turnover Rate & Survey Score by Store</div>
          </div>
          <div style="height:320px; position:relative;">
            <canvas id="staffScatterChart"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">🚪 Primary Reasons for Staff Departure (Exit Survey)</div>
          </div>
          <div style="height:320px; position:relative;">
            <canvas id="exitReasonChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Interactive Shift / Rota Simulator -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">⏰ Interactive Shift Timing & Lunch Rush Simulator</div>
            <div class="card-subtitle">Test reallocating staffing hours into peak lunchtime (11:30–13:30) to eliminate queue abandonments</div>
          </div>
        </div>
        <div class="grid-2">
          <div>
            <div style="margin-bottom:1rem;">
              <label style="font-weight:600; font-size:0.85rem; display:block; margin-bottom:0.4rem;">Select Bottleneck Store:</label>
              <select id="sim-rota-store" onchange="runRotaSim()">
                <option value="S07">S07 - Manchester Piccadilly (5-deep queues, high walkouts)</option>
                <option value="S06">S06 - Manchester Spinningfields (30-min office lunch limit)</option>
                <option value="S10">S10 - Hull Paragon (Staff doing cleaning duties)</option>
                <option value="S03">S03 - Leeds Briggate (Weekend peak seating)</option>
              </select>
            </div>

            <div class="slider-group">
              <div class="slider-header">
                <span>Hours Reallocated to Peak Lunch Rush (Daily)</span>
                <span class="slider-val" id="val-rota-hours">4.0 hrs/day</span>
              </div>
              <input type="range" id="slider-rota-hours" min="1" max="8" step="0.5" value="4" oninput="runRotaSim()">
            </div>

            <div class="slider-group">
              <div class="slider-header">
                <span>Peak Shift Wage Top-up Premium (£/hr)</span>
                <span class="slider-val" id="val-rota-wage">+£0.50/hr</span>
              </div>
              <input type="range" id="slider-rota-wage" min="0" max="1.50" step="0.25" value="0.50" oninput="runRotaSim()">
            </div>
          </div>

          <div style="padding:1.25rem; background:var(--card-hover); border-radius:12px; display:flex; flex-direction:column; justify-content:center; gap:0.85rem;">
            <div>
              <div style="font-size:0.8rem; color:var(--text-muted);">Queue Walkout Rate Reduction:</div>
              <div style="font-size:1.5rem; font-weight:800; color:var(--emerald);" id="rota-sim-walkout">-65% Walkouts</div>
            </div>
            <div>
              <div style="font-size:0.8rem; color:var(--text-muted);">Recaptured Annual Sales (Walk-ins served):</div>
              <div style="font-size:1.5rem; font-weight:800; color:var(--accent);" id="rota-sim-sales">+£58,400 / yr</div>
            </div>
            <div>
              <div style="font-size:0.8rem; color:var(--text-muted);">Net Incremental Profit (After wage premium):</div>
              <div style="font-size:1.5rem; font-weight:800; color:var(--emerald);" id="rota-sim-profit">+£39,200 / yr</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: WASTE MANAGEMENT -->
    <div id="tab-waste" class="tab-content">
      
      <!-- AI Waste Suggestions -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">AI Waste Reduction Audit</span>
          <span class="ai-box-title">Cutting £133,815 in Annual Food Wastage</span>
        </div>
        <ul>
          <li><strong>Bakery Waste (£52,367 — 11.7% waste rate):</strong> Croissants, pain au chocolat, and muffins suffer high end-of-day discard because head office par levels are static across all seasons.</li>
          <li><strong>Lunch Items (£68,162 — 8.8% waste rate):</strong> Sandwiches and baguettes represent the single highest cash waste due to short 1-day shelf life. Marcus Dyer at Hull admits to intentionally over-ordering safety stock.</li>
          <li><strong>3 Actionable Waste Solutions:</strong>
            1) Roll out dynamic par levels tied to live 3-day weather and footfall forecasts (saves ~£40k/yr).
            2) App 15:00 "Happy Hour" dynamic 40% markdowns on expiring bakery goods.
            3) Too Good To Go surplus "Magic Bags" to recover ingredient cost on remaining items.
          </li>
        </ul>
      </div>

      <!-- Waste Categories Grid -->
      <div class="grid-3">
        <div class="kpi-card rose">
          <div class="kpi-label">Lunch Category Waste</div>
          <div class="kpi-value text-rose">£68,162</div>
          <div class="kpi-sub"><span class="badge badge-rose">29,148 units wasted (8.8%)</span></div>
        </div>

        <div class="kpi-card amber">
          <div class="kpi-label">Bakery Category Waste</div>
          <div class="kpi-value text-amber">£52,367</div>
          <div class="kpi-sub"><span class="badge badge-amber">52,652 units wasted (11.7%)</span></div>
        </div>

        <div class="kpi-card emerald">
          <div class="kpi-label">Breakfast Category Waste</div>
          <div class="kpi-value text-emerald">£13,286</div>
          <div class="kpi-sub"><span class="badge badge-emerald">7,899 units wasted (6.7%)</span></div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">🗑️ Annual Food Waste Cost by Store (£ GBP)</div>
            <div class="card-subtitle">Leeds Briggate, Hull Paragon, and Piccadilly have highest wastage</div>
          </div>
          <div style="height:320px; position:relative;">
            <canvas id="storeWasteChart"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">📋 Store Waste Breakdown Table</div>
          </div>
          <div class="table-container" style="max-height:320px; overflow-y:auto;">
            <table id="waste-table">
              <thead>
                <tr>
                  <th>Store</th>
                  <th class="text-right">Prepared</th>
                  <th class="text-right">Wasted</th>
                  <th class="text-right">Waste %</th>
                  <th class="text-right">Cost Wasted</th>
                </tr>
              </thead>
              <tbody id="waste-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 8: FUTURE INVESTMENTS (THE £1.5M ALLOCATION) -->
    <div id="tab-investments" class="tab-content">
      
      <!-- AI Investment Strategy -->
      <div class="ai-box">
        <div class="ai-box-header">
          <span class="ai-badge">Board Strategic Advisory</span>
          <span class="ai-box-title">Data-Driven Capital Allocation for the £1,500,000 Budget</span>
        </div>
        <p style="font-size:0.88rem; line-height:1.55; margin-bottom:0.6rem;">
          Anna Whitfield has £1.5M to invest. She instinctively favored <em>Sheffield Kelham Island (CS2)</em> and <em>Leeds Wellington Place (CS7)</em> ("Leeds has been good to us"). <strong>The data reveals this would be a catastrophic mistake:</strong>
        </p>
        <ul>
          <li><strong>AVOID Leeds Wellington Place (CS7) — THE CANNIBALIZATION TRAP:</strong> Quoted rent is high (£11.8k/mo), street footfall is weak (9,500), and Leeds already has Briggate and Trinity within 0.5 miles! Opening Wellington Place leads to a <strong>projected loss of -£82,414/yr</strong> with a 99-year payback!</li>
          <li><strong>AVOID Sheffield Kelham Island (CS2):</strong> £390k fitout on low street footfall (14.5k) yields an abysmal 25.3-year payback and 3.4% margin.</li>
          <li><strong>DEPLOY CAPITAL INTO PROVEN WINNERS:</strong>
            1) <strong>Manchester Oxford Road (CS3)</strong>: 52k daily footfall, 31k students, £240k fitout = <strong>1.2-year payback</strong> (+£192k EBITDA/yr).
            2) <strong>York Station Kiosk (CS4)</strong>: £180k fitout, replicable transit kiosk model = <strong>1.3-year payback</strong> (+£135k EBITDA/yr).
            3) <strong>Leeds Headingley (CS1)</strong>: Suburban student high street far from city centre = <strong>2.4-year payback</strong> (+£134k EBITDA/yr).
          </li>
        </ul>
      </div>

      <!-- Candidate Sites Table -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">🏢 Candidate Sites Investment Appraisal Matrix</div>
            <div class="card-subtitle">Evaluated against catchment demographics, footfall, fitout, and cannibalization risk</div>
          </div>
        </div>
        <div class="table-container">
          <table id="candidate-sites-table">
            <thead>
              <tr>
                <th>Site ID</th>
                <th>Candidate Name</th>
                <th>City</th>
                <th>Location Type</th>
                <th class="text-right">Fitout Cost</th>
                <th class="text-right">Rent / Mo</th>
                <th class="text-right">Footfall</th>
                <th class="text-right">Est EBITDA</th>
                <th class="text-right">Payback</th>
                <th>Cannibalization Risk</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody id="candidate-sites-tbody"></tbody>
          </table>
        </div>
      </div>

      <!-- Interactive Capital Allocator (£1.5M) -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">🧮 Interactive £1,500,000 Capital Allocation Planner</div>
            <div class="card-subtitle">Select projects to model portfolio EBITDA and payback</div>
          </div>
          <div>
            <button class="btn btn-primary" onclick="resetRecommendedBudget()">Reset to Recommended Portfolio</button>
          </div>
        </div>

        <div class="grid-2">
          <div id="budget-items-list" style="display:flex; flex-direction:column; gap:0.6rem;">
            <!-- Rendered via JS -->
          </div>

          <div style="padding:1.5rem; background:var(--card-hover); border-radius:12px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase; color:var(--text-muted); margin-bottom:0.5rem;">Budget Utilization</div>
              <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                <span style="font-size:1.1rem; font-weight:800;" id="budget-spent-val">£1,500,000 / £1,500,000</span>
                <span style="font-size:1.1rem; font-weight:800; color:var(--emerald);" id="budget-remaining-val">£0 Remaining</span>
              </div>
              <div style="height:10px; background:var(--card-border); border-radius:5px; overflow:hidden; margin-bottom:1.25rem;">
                <div id="budget-progress-bar" style="height:100%; width:100%; background:var(--emerald); transition:all 0.3s;"></div>
              </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1rem;">
              <div style="padding:1rem; background:var(--card-bg); border-radius:10px; border:1px solid var(--card-border);">
                <div style="font-size:0.75rem; color:var(--text-muted);">Projected Incremental Annual EBITDA:</div>
                <div style="font-size:1.5rem; font-weight:800; color:var(--emerald);" id="budget-total-ebitda">+£691,431 / yr</div>
                <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.25rem;">+64.8% growth in chain profit!</div>
              </div>

              <div style="padding:1rem; background:var(--card-bg); border-radius:10px; border:1px solid var(--card-border);">
                <div style="font-size:0.75rem; color:var(--text-muted);">Blended Portfolio Payback:</div>
                <div style="font-size:1.5rem; font-weight:800; color:var(--accent);" id="budget-blended-payback">2.17 Years</div>
                <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.25rem;">Highly accretive capital return</div>
              </div>
            </div>

            <div style="font-size:0.8rem; line-height:1.45; color:var(--text-muted);">
              💡 <em>This balanced allocation transforms Grind & Crumb by capturing high student & transit footfall, unclogging the Piccadilly delivery bottleneck, refitting top flagship York Stonegate, and securing operational reserves.</em>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 9: UPLOAD NEW DATA -->
    <div id="tab-upload" class="tab-content">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">📤 Upload New Store or Operational Data</div>
            <div class="card-subtitle">Upload new CSV files (e.g. daily sales, waste logs, staff rota) to dynamically recalculate KPIs and models.</div>
          </div>
        </div>

        <div class="dropzone" id="dropzone" onclick="document.getElementById('file-input').click()">
          <input type="file" id="file-input" style="display:none;" accept=".csv" onchange="handleFileUpload(event)">
          <div style="font-size:2.5rem; margin-bottom:0.5rem;">📁</div>
          <div style="font-weight:700; font-size:1.1rem; margin-bottom:0.3rem;">Drag & drop your CSV file here, or click to browse</div>
          <div style="font-size:0.85rem; color:var(--text-muted);">Supports daily_store_sales.csv, waste_log.csv, staff_rota_weekly.csv, etc.</div>
        </div>

        <div id="upload-status" style="margin-top:1rem; display:none;"></div>
      </div>
    </div>

  </main>

  <!-- Interactive CEO AI Chatbot Drawer -->
  <div class="chat-drawer" id="chatDrawer">
    <div class="chat-header">
      <div style="display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:1.2rem;">🤖</span>
        <div>
          <div style="font-weight:700; font-size:0.95rem;">CEO Strategic AI Assistant</div>
          <div style="font-size:0.72rem; opacity:0.9;">Powered by Gemini & Grind and Crumb Intelligence</div>
        </div>
      </div>
      <button onclick="toggleChat()" style="background:transparent; border:none; color:white; font-size:1.2rem; cursor:pointer;">✕</button>
    </div>

    <div class="chat-body" id="chatBody">
      <div class="chat-msg bot">
        Hello Anna. I have fully indexed all 12 stores, candidate sites, staff rotas, waste logs, and delivery platform terms. What strategic question can I answer for you?
      </div>
    </div>

    <div style="padding:0.5rem 1rem 0 1rem; background:var(--card-bg);">
      <div class="prompt-chips">
        <span class="prompt-chip" onclick="askPredefined('Why is Manchester Piccadilly losing money?')">Why is Piccadilly losing?</span>
        <span class="prompt-chip" onclick="askPredefined('Where should I allocate the £1.5M budget?')">Where to allocate £1.5M?</span>
        <span class="prompt-chip" onclick="askPredefined('Should we open Leeds Wellington Place?')">Open Wellington Place?</span>
        <span class="prompt-chip" onclick="askPredefined('How do we reduce waste at Leeds Briggate?')">Cut Briggate waste?</span>
        <span class="prompt-chip" onclick="askPredefined('Should we scrap the oat milk surcharge?')">Scrap oat milk fee?</span>
      </div>
    </div>

    <div class="chat-footer">
      <input type="text" id="chatInput" placeholder="Ask about stores, profit, rotas, sites..." style="flex:1;" onkeypress="if(event.key==='Enter') sendChatMessage()">
      <button class="btn btn-primary" onclick="sendChatMessage()">Send</button>
    </div>
  </div>

  <!-- Embedded Dashboard Data & Logic -->
  <script>
    const INITIAL_DATA = {data_json};
    let currentData = INITIAL_DATA;
    let selectedStoreId = 'S07';

    // Theme toggle
    function toggleTheme() {{
      const html = document.documentElement;
      const btn = document.getElementById('themeBtn');
      if (html.classList.contains('dark')) {{
        html.classList.remove('dark');
        html.classList.add('light');
        btn.innerText = '🌙 Dark';
      }} else {{
        html.classList.remove('light');
        html.classList.add('dark');
        btn.innerText = '☀️ Light';
      }}
    }}

    // Tab switcher
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      
      const target = document.getElementById('tab-' + tabId);
      if (target) target.classList.add('active');

      const tabs = document.querySelectorAll('.nav-tab');
      const map = ['overview', 'stores', 'costs', 'income', 'delivery', 'staff', 'waste', 'investments', 'upload'];
      const idx = map.indexOf(tabId);
      if (idx !== -1 && tabs[idx]) tabs[idx].classList.add('active');

      // Trigger redraw of charts on tab activate
      setTimeout(() => {{
        window.dispatchEvent(new Event('resize'));
      }}, 50);
    }}

    // Toggle Chat
    function toggleChat() {{
      const drawer = document.getElementById('chatDrawer');
      drawer.classList.toggle('open');
      if (drawer.classList.contains('open')) {{
        document.getElementById('chatInput').focus();
      }}
    }}

    // 1. Populate Overview Table
    function renderOverviewTable(filter = 'ALL') {{
      const tbody = document.getElementById('overview-tbody');
      tbody.innerHTML = '';

      let stores = [...currentData.stores];
      // Sort least profit (most loss) to most profit
      stores.sort((a, b) => a.profit - b.profit);

      if (filter !== 'ALL') {{
        stores = stores.filter(s => s.status === filter);
      }}

      stores.forEach(s => {{
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.onclick = (e) => {{
          if (e.target.tagName !== 'BUTTON') {{
            selectStoreAndOpen(s.store_id);
          }}
        }};

        const profitClass = s.profit >= 0 ? 'text-emerald' : 'text-rose';
        const badgeClass = s.status === 'Performing Well' ? 'badge-emerald' : (s.status === 'Middle Performing' ? 'badge-amber' : 'badge-rose');

        tr.innerHTML = `
          <td>
            <div style="font-weight:700;">${{s.store_name}}</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">${{s.store_id}} · Mgr: ${{s.store_manager}}</div>
          </td>
          <td>
            <div>${{s.city}}</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">${{s.format}} (${{s.location_type}})</div>
          </td>
          <td class="text-right font-mono font-semibold">£${{s.sales.total.toLocaleString()}}</td>
          <td class="text-right font-mono">£${{s.costs.rent.toLocaleString()}}</td>
          <td class="text-right font-mono">£${{s.costs.labour.toLocaleString()}}</td>
          <td class="text-right font-mono text-amber">£${{s.waste.cost_wasted.toLocaleString()}}</td>
          <td class="text-right font-mono font-semibold ${{profitClass}}">
            ${{s.profit < 0 ? '-' : ''}}£${{Math.abs(s.profit).toLocaleString()}}
          </td>
          <td class="text-right font-mono font-semibold ${{profitClass}}">${{s.margin.toFixed(1)}}%</td>
          <td class="text-center">
            <span class="badge ${{badgeClass}}">${{s.status}}</span>
          </td>
          <td class="text-center">
            <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem;" onclick="selectStoreAndOpen('${{s.store_id}}')">Inspect</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filterOverviewTable() {{
      const filter = document.getElementById('overview-filter').value;
      renderOverviewTable(filter);
    }}

    function selectStoreAndOpen(storeId) {{
      selectedStoreId = storeId;
      document.getElementById('store-selector').value = storeId;
      renderStoreDeepDive();
      switchTab('stores');
    }}

    // Charts references
    let profitRankChart = null;
    let monthlyTrendChart = null;
    let storeIndividualChart = null;
    let costDoughnutChart = null;
    let deliveryBasketChart = null;
    let staffScatterChart = null;
    let exitReasonChart = null;
    let storeWasteChart = null;

    // Render Overview Charts
    function renderOverviewCharts() {{
      const stores = [...currentData.stores].sort((a, b) => a.profit - b.profit);
      const labels = stores.map(s => s.store_name.replace('Manchester ', 'Mcr ').replace('Sheffield ', 'Sheff '));
      const profits = stores.map(s => s.profit);
      const colors = stores.map(s => s.profit >= 0 ? '#10b981' : '#ef4444');

      const ctx1 = document.getElementById('profitRankChart');
      if (ctx1) {{
        if (profitRankChart) profitRankChart.destroy();
        profitRankChart = new Chart(ctx1, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              label: 'Annual Operating Profit / Loss (£)',
              data: profits,
              backgroundColor: colors,
              borderRadius: 6
            }}]
          }},
          options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: (ctx) => ' Profit: £' + Math.round(ctx.raw).toLocaleString()
                }}
              }}
            }},
            scales: {{
              x: {{
                grid: {{ color: 'rgba(255,255,255,0.06)' }},
                ticks: {{
                  callback: (v) => '£' + (v/1000) + 'k'
                }}
              }},
              y: {{
                grid: {{ display: false }},
                ticks: {{ font: {{ size: 11 }} }}
              }}
            }}
          }}
        }});
      }}

      updateMonthlyProfitChart();
    }}

    function updateMonthlyProfitChart() {{
      const sel = document.getElementById('chart-store-select').value;
      const ctx2 = document.getElementById('monthlyTrendChart');
      if (!ctx2) return;

      const months = currentData.chain_monthly_trend.map(m => m.month);

      let datasets = [];
      if (sel === 'ALL') {{
        // Show S07 (Piccadilly), S03 (Briggate), S12 (Trinity), S04 (York)
        const targetIds = ['S07', 'S03', 'S12', 'S04'];
        const lineColors = {{ 'S07': '#ef4444', 'S03': '#f59e0b', 'S12': '#8b5cf6', 'S04': '#10b981' }};
        targetIds.forEach(id => {{
          const s = currentData.stores.find(x => x.store_id === id);
          if (s) {{
            datasets.push({{
              label: s.store_name,
              data: s.monthly_trend.map(t => t.profit),
              borderColor: lineColors[id],
              backgroundColor: lineColors[id],
              tension: 0.25,
              borderWidth: 2
            }});
          }}
        }});
      }} else {{
        const s = currentData.stores.find(x => x.store_id === sel);
        if (s) {{
          datasets.push({{
            label: s.store_name + ' Monthly Profit (£)',
            data: s.monthly_trend.map(t => t.profit),
            borderColor: s.profit >= 0 ? '#10b981' : '#ef4444',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.25,
            borderWidth: 2
          }});
        }}
      }}

      if (monthlyTrendChart) monthlyTrendChart.destroy();
      monthlyTrendChart = new Chart(ctx2, {{
        type: 'line',
        data: {{
          labels: months,
          datasets: datasets
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'top', labels: {{ boxWidth: 12 }} }}
          }},
          scales: {{
            y: {{
              grid: {{ color: 'rgba(255,255,255,0.06)' }},
              ticks: {{ callback: (v) => '£' + (v/1000) + 'k' }}
            }},
            x: {{
              grid: {{ display: false }}
            }}
          }}
        }}
      }});
    }}

    // 2. Store Deep Dive
    function populateStoreSelector() {{
      const sel = document.getElementById('store-selector');
      sel.innerHTML = '';
      currentData.stores.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s.store_id;
        opt.innerText = `${{s.store_id}} - ${{s.store_name}} (${{s.status}})`;
        if (s.store_id === selectedStoreId) opt.selected = true;
        sel.appendChild(opt);
      }});
    }}

    function renderStoreDeepDive() {{
      selectedStoreId = document.getElementById('store-selector').value;
      const s = currentData.stores.find(x => x.store_id === selectedStoreId);
      if (!s) return;

      // Banner
      const banner = document.getElementById('store-detail-banner');
      const badgeClass = s.status === 'Performing Well' ? 'badge-emerald' : (s.status === 'Middle Performing' ? 'badge-amber' : 'badge-rose');
      banner.innerHTML = `
        <div class="ai-box-header">
          <span class="badge ${{badgeClass}}">${{s.status}}</span>
          <span class="ai-box-title">${{s.store_name}} — ${{s.ai_diagnostic.headline}}</span>
        </div>
        <p style="font-size:0.87rem; line-height:1.55; margin-bottom:0.75rem;">
          ${{s.ai_diagnostic.why_underperforming}}
        </p>
        <div style="font-weight:700; font-size:0.85rem; margin-bottom:0.35rem; color:var(--accent);">Turnaround Action Plan:</div>
        <ul>
          ${{s.ai_diagnostic.actionable_recommendations.map(r => `<li>${{r}}</li>`).join('')}}
        </ul>
      `;

      // KPI Grid
      const kpis = document.getElementById('store-kpi-grid');
      const profitColor = s.profit >= 0 ? 'emerald' : 'rose';
      kpis.innerHTML = `
        <div class="kpi-card">
          <div class="kpi-label">Annual Revenue</div>
          <div class="kpi-value">£${{s.sales.total.toLocaleString()}}</div>
          <div class="kpi-sub">${{s.orders.total.toLocaleString()}} total orders</div>
        </div>
        <div class="kpi-card ${{profitColor}}">
          <div class="kpi-label">Net Profit / Loss</div>
          <div class="kpi-value text-${{profitColor}}">${{s.profit < 0 ? '-' : ''}}£${{Math.abs(s.profit).toLocaleString()}}</div>
          <div class="kpi-sub">${{s.margin.toFixed(1)}}% Net Margin</div>
        </div>
        <div class="kpi-card rose">
          <div class="kpi-label">Property Rent</div>
          <div class="kpi-value">£${{s.costs.rent.toLocaleString()}}</div>
          <div class="kpi-sub">£${{s.rent_gbp_month.toLocaleString()}}/mo · ${{((s.costs.rent / s.sales.total)*100).toFixed(1)}}% of sales</div>
        </div>
        <div class="kpi-card amber">
          <div class="kpi-label">Staff Turnover Rate</div>
          <div class="kpi-value text-amber">${{s.staff.turnover_rate_pct}}%</div>
          <div class="kpi-sub">${{s.staff.leavers}} leavers · Score: ${{s.staff.avg_survey_score}}/10</div>
        </div>
      `;

      // P&L Table
      const pnl = document.getElementById('store-pnl-table');
      pnl.innerHTML = `
        <tr><td><strong>Net Sales (Revenue)</strong></td><td class="text-right font-mono font-semibold">£${{s.sales.total.toLocaleString()}}</td></tr>
        <tr><td style="padding-left:1.5rem; color:var(--text-muted);">In-Store Sales (69%)</td><td class="text-right font-mono">£${{s.sales.instore.toLocaleString()}}</td></tr>
        <tr><td style="padding-left:1.5rem; color:var(--text-muted);">Delivery Platform Sales (18%)</td><td class="text-right font-mono">£${{s.sales.delivery.toLocaleString()}}</td></tr>
        <tr><td style="padding-left:1.5rem; color:var(--text-muted);">App Click & Collect (13%)</td><td class="text-right font-mono">£${{s.sales.app.toLocaleString()}}</td></tr>
        <tr style="background:var(--card-hover);"><td><strong>Cost of Goods Sold (Ingredients)</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.cogs_ingredients.toLocaleString()}}</td></tr>
        <tr><td><strong>Labour Cost (Rota x Wage x 1.13)</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.labour.toLocaleString()}}</td></tr>
        <tr><td><strong>Property Rent</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.rent.toLocaleString()}}</td></tr>
        <tr><td><strong>Business Rates</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.rates.toLocaleString()}}</td></tr>
        <tr><td><strong>Utilities (Gas, Electric, Water)</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.utilities.toLocaleString()}}</td></tr>
        <tr><td><strong>Repairs & Maintenance</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.repairs.toLocaleString()}}</td></tr>
        <tr><td><strong>Consumables / Hygiene / Other Opex</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.other_opex.toLocaleString()}}</td></tr>
        <tr><td><strong>Delivery Commissions & Packaging</strong></td><td class="text-right font-mono text-rose">-£${{s.costs.delivery_total.toLocaleString()}}</td></tr>
        <tr style="border-top:2px solid var(--card-border); background:var(--card-hover);">
          <td><strong>NET OPERATING PROFIT / (LOSS)</strong></td>
          <td class="text-right font-mono font-semibold text-${{profitColor}}">${{s.profit < 0 ? '-' : ''}}£${{Math.abs(s.profit).toLocaleString()}} (${{s.margin.toFixed(1)}}%)</td>
        </tr>
      `;

      // Store Monthly Trend Chart
      const ctx = document.getElementById('storeIndividualChart');
      if (ctx) {{
        if (storeIndividualChart) storeIndividualChart.destroy();
        storeIndividualChart = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: s.monthly_trend.map(m => m.month),
            datasets: [
              {{
                type: 'line',
                label: 'Monthly Net Profit (£)',
                data: s.monthly_trend.map(m => m.profit),
                borderColor: s.profit >= 0 ? '#10b981' : '#ef4444',
                borderWidth: 2,
                tension: 0.2
              }},
              {{
                type: 'bar',
                label: 'Monthly Revenue (£)',
                data: s.monthly_trend.map(m => m.sales),
                backgroundColor: 'rgba(59, 130, 246, 0.4)',
                borderRadius: 4
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{
              y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }} }}
            }}
          }}
        }});
      }}

      // Rota breakdown
      const rotaBox = document.getElementById('store-rota-summary');
      rotaBox.innerHTML = `
        <div style="font-size:0.85rem; line-height:1.6;">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Morning (07-11):</span>
            <span class="font-mono">${{s.staff.daypart_hours.Morning || 0}} hrs</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Lunch Peak (11-14):</span>
            <span class="font-mono font-semibold text-accent">${{s.staff.daypart_hours.Lunch || 0}} hrs</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Afternoon (14-18):</span>
            <span class="font-mono">${{s.staff.daypart_hours.Afternoon || 0}} hrs</span>
          </div>
          <div style="margin-top:0.75rem; padding-top:0.75rem; border-top:1px solid var(--card-border); font-size:0.78rem; color:var(--text-muted);">
            Avg Hourly Wage: £12.40 - £13.40 · Headcount: ${{s.staff.headcount}}
          </div>
        </div>
      `;

      // Footfall breakdown
      const footBox = document.getElementById('store-footfall-summary');
      footBox.innerHTML = `
        <div style="font-size:0.85rem; line-height:1.6;">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Annual Door Count:</span>
            <span class="font-mono font-semibold">${{s.footfall.annual_door_count.toLocaleString()}}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Store Seating Capacity:</span>
            <span class="font-mono">${{s.seats}} seats (${{s.sqft}} sqft)</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Footfall Conversion Rate:</span>
            <span class="font-mono text-emerald">${{s.footfall.conversion_rate_pct}}%</span>
          </div>
        </div>
      `;

      // Reviews summary
      const revBox = document.getElementById('store-reviews-summary');
      revBox.innerHTML = `
        <div style="font-size:0.85rem; line-height:1.6;">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Average Review Rating:</span>
            <span class="font-mono font-semibold text-amber">${{s.customer.avg_rating}} / 5.0 ⭐</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Queue / Wait Time Complaints:</span>
            <span class="font-mono text-rose">${{s.customer.complaints.wait_time || 0}} mentions</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span>Oat Milk Surcharge Complaints:</span>
            <span class="font-mono text-amber">${{s.customer.complaints.oat_milk || 0}} mentions</span>
          </div>
        </div>
      `;
    }}

    // 3. Costs Cards & Breakdown
    function renderCostsTab() {{
      const c = currentData.chain;
      const grid = document.getElementById('costs-cards-grid');
      const costs = [
        {{ label: 'Labour Cost (Staff Rota)', val: c.total_labour, pct: ((c.total_labour/c.total_expenses)*100).toFixed(1), color: 'purple', sub: 'Scheduled hours x wage x 1.13' }},
        {{ label: 'Cost of Goods Sold (Ingredients)', val: c.total_cogs, pct: ((c.total_cogs/c.total_expenses)*100).toFixed(1), color: 'rose', sub: 'Food & beverage unit cost' }},
        {{ label: 'Property Rent', val: c.total_rent, pct: ((c.total_rent/c.total_expenses)*100).toFixed(1), color: 'amber', sub: 'Across 12 commercial leases' }},
        {{ label: 'Delivery Commission & Packaging', val: c.total_delivery_costs, pct: ((c.total_delivery_costs/c.total_expenses)*100).toFixed(1), color: 'rose', sub: 'RushEats & Dashly commissions' }},
        {{ label: 'Utilities (Gas / Electric / Water)', val: c.total_utilities, pct: ((c.total_utilities/c.total_expenses)*100).toFixed(1), color: 'blue', sub: 'Commercial utilities bills' }},
        {{ label: 'Business Rates', val: c.total_rates, pct: ((c.total_rates/c.total_expenses)*100).toFixed(1), color: 'blue', sub: 'Local council business rates' }},
        {{ label: 'Consumables & Hygiene Opex', val: c.total_other_opex, pct: ((c.total_other_opex/c.total_expenses)*100).toFixed(1), color: 'amber', sub: 'Cleaning chemicals, napkins, packaging' }},
        {{ label: 'Repairs & Maintenance', val: c.total_repairs, pct: ((c.total_repairs/c.total_expenses)*100).toFixed(1), color: 'rose', sub: 'Boiler, dishwasher, espresso machine' }},
        {{ label: 'Historical Capex (Refits/Fitouts)', val: 860000, pct: '11.3', color: 'purple', sub: 'S12 fitout £385k, S03 refit £210k' }}
      ];

      grid.innerHTML = costs.map(item => `
        <div class="kpi-card ${{item.color}}">
          <div class="kpi-label">${{item.label}}</div>
          <div class="kpi-value">£${{item.val.toLocaleString()}}</div>
          <div class="kpi-sub">
            <span class="badge badge-${{item.color}}">${{item.pct}}% of costs</span>
            <span>${{item.sub}}</span>
          </div>
        </div>
      `).join('');

      // Doughnut chart
      const ctx = document.getElementById('costDoughnutChart');
      if (ctx) {{
        if (costDoughnutChart) costDoughnutChart.destroy();
        costDoughnutChart = new Chart(ctx, {{
          type: 'doughnut',
          data: {{
            labels: ['Labour', 'Ingredients (COGS)', 'Rent', 'Delivery Fees', 'Utilities', 'Rates', 'Other Opex', 'Repairs'],
            datasets: [{{
              data: [c.total_labour, c.total_cogs, c.total_rent, c.total_delivery_costs, c.total_utilities, c.total_rates, c.total_other_opex, c.total_repairs],
              backgroundColor: ['#8b5cf6', '#ef4444', '#f59e0b', '#ec4899', '#3b82f6', '#06b6d4', '#10b981', '#64748b']
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ position: 'right', labels: {{ boxWidth: 12 }} }}
            }}
          }}
        }});
      }}
    }}

    function runCostSim() {{
      let savings = 0;
      if (document.getElementById('sim-dashly').checked) savings += 22500;
      if (document.getElementById('sim-small-order').checked) savings += 38000;
      if (document.getElementById('sim-par-waste').checked) savings += 40140;
      if (document.getElementById('sim-boiler').checked) savings += 8000;
      if (document.getElementById('sim-consumables').checked) savings += 15000;

      document.getElementById('sim-total-savings').innerText = '£' + savings.toLocaleString() + ' / year';
    }}

    // 4. Income & Menu ROI
    function renderIncomeTab() {{
      const prods = currentData.products;
      const topTbody = document.getElementById('top-products-tbody');
      const botTbody = document.getElementById('bottom-products-tbody');
      const fullTbody = document.getElementById('full-menu-tbody');

      topTbody.innerHTML = '';
      botTbody.innerHTML = '';
      fullTbody.innerHTML = '';

      // Top 10
      prods.slice(0, 10).forEach(p => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{p.product_name}}</strong></td>
          <td><span class="badge badge-blue">${{p.category}}</span></td>
          <td class="text-right font-mono">£${{p.menu_price_gbp.toFixed(2)}}</td>
          <td class="text-right font-mono text-emerald font-semibold">${{p.margin_pct.toFixed(1)}}%</td>
          <td class="text-right font-mono font-semibold">£${{p.annual_revenue.toLocaleString()}}</td>
        `;
        topTbody.appendChild(tr);
      }});

      // Bottom 10
      prods.slice(-10).reverse().forEach(p => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{p.product_name}}</strong></td>
          <td><span class="badge badge-amber">${{p.category}}</span></td>
          <td class="text-right font-mono">£${{p.menu_price_gbp.toFixed(2)}}</td>
          <td class="text-right font-mono">${{p.margin_pct.toFixed(1)}}%</td>
          <td class="text-right font-mono font-semibold">£${{p.annual_revenue.toLocaleString()}}</td>
        `;
        botTbody.appendChild(tr);
      }});

      // Full Menu Items Table
      prods.forEach(p => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="font-mono text-muted">${{p.product_id}}</td>
          <td><strong>${{p.product_name}}</strong></td>
          <td>${{p.category}}</td>
          <td class="text-right font-mono">£${{p.menu_price_gbp.toFixed(2)}}</td>
          <td class="text-right font-mono">£${{p.unit_cost_gbp.toFixed(2)}}</td>
          <td class="text-right font-mono text-emerald">£${{p.unit_margin_gbp.toFixed(2)}}</td>
          <td class="text-right font-mono font-semibold text-emerald">${{p.margin_pct.toFixed(1)}}%</td>
          <td class="text-right font-mono">${{p.annual_qty.toLocaleString()}}</td>
          <td class="text-right font-mono font-semibold">£${{p.annual_profit.toLocaleString()}}</td>
          <td class="text-right font-mono text-accent font-semibold">${{p.roi_pct.toFixed(0)}}%</td>
        `;
        fullTbody.appendChild(tr);
      }});
    }}

    // 5. Delivery Hub & Calculator
    function renderDeliveryTab() {{
      const b = currentData.delivery_summary.orders_by_bracket;
      const ctx = document.getElementById('deliveryBasketChart');
      if (ctx) {{
        if (deliveryBasketChart) deliveryBasketChart.destroy();
        deliveryBasketChart = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: ['Under £8 (Loss risk)', '£8 - £15 (Standard)', '£15 - £25 (Multi-item)', 'Over £25 (Office group)'],
            datasets: [{{
              label: 'Sample Orders',
              data: [b.under_8, b['8_to_15'], b['15_to_25'], b.over_25],
              backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#8b5cf6'],
              borderRadius: 6
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }}
          }}
        }});
      }}
      calcDeliveryEconomics();
    }}

    function calcDeliveryEconomics() {{
      const minBasket = parseFloat(document.getElementById('slider-min-basket').value);
      const smallFee = parseFloat(document.getElementById('slider-small-fee').value);
      const commRate = parseFloat(document.getElementById('slider-comm-rate').value) / 100.0;
      const markup = parseFloat(document.getElementById('slider-del-markup').value) / 100.0;

      document.getElementById('val-min-basket').innerText = '£' + minBasket.toFixed(2);
      document.getElementById('val-small-fee').innerText = '£' + smallFee.toFixed(2);
      document.getElementById('val-comm-rate').innerText = (commRate * 100).toFixed(1) + '%';
      document.getElementById('val-del-markup').innerText = (markup * 100).toFixed(0) + '%';

      // Base order: £12.67 avg AOV
      const effectiveAov = 12.67 * (1.0 + markup * 0.5) + (smallFee * 0.29);
      const commCost = effectiveAov * commRate;
      const packCost = 0.45;
      const cogs = effectiveAov * 0.274;
      const labourTimeCost = 0.87; // 4 mins barista time

      const netProfitOrder = effectiveAov - commCost - packCost - cogs - labourTimeCost;
      const netMargin = (netProfitOrder / effectiveAov) * 100;

      // Base net profit order was ~£2.80
      const upliftPerOrder = Math.max(0, netProfitOrder - 2.80);
      const annualUplift = upliftPerOrder * 111000; // approx 111k annual orders

      document.getElementById('calc-net-order-profit').innerText = '£' + netProfitOrder.toFixed(2);
      document.getElementById('calc-net-order-margin').innerText = netMargin.toFixed(1) + '%';
      document.getElementById('calc-annual-delivery-uplift').innerText = '+£' + Math.round(annualUplift).toLocaleString() + ' / yr';
    }}

    // 6. Staff Tab & Simulator
    function renderStaffTab() {{
      const stores = currentData.stores;
      const ctx1 = document.getElementById('staffScatterChart');
      if (ctx1) {{
        if (staffScatterChart) staffScatterChart.destroy();
        staffScatterChart = new Chart(ctx1, {{
          type: 'bar',
          data: {{
            labels: stores.map(s => s.store_id),
            datasets: [
              {{
                label: 'Turnover Rate %',
                data: stores.map(s => s.staff.turnover_rate_pct),
                backgroundColor: stores.map(s => s.staff.turnover_rate_pct > 100 ? '#ef4444' : '#f59e0b'),
                borderRadius: 4
              }},
              {{
                label: 'Survey Score (out of 10)',
                data: stores.map(s => s.staff.avg_survey_score * 10), // scale for visual comparison
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderRadius: 4
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false
          }}
        }});
      }}

      // Exit reasons
      const ctx2 = document.getElementById('exitReasonChart');
      if (ctx2) {{
        const reasons = currentData.staff_exit_reasons;
        if (exitReasonChart) exitReasonChart.destroy();
        exitReasonChart = new Chart(ctx2, {{
          type: 'doughnut',
          data: {{
            labels: Object.keys(reasons),
            datasets: [{{
              data: Object.values(reasons),
              backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#64748b']
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ position: 'right' }} }}
          }}
        }});
      }}

      runRotaSim();
    }}

    function runRotaSim() {{
      const hrs = parseFloat(document.getElementById('slider-rota-hours').value);
      const wageTopup = parseFloat(document.getElementById('slider-rota-wage').value);

      document.getElementById('val-rota-hours').innerText = hrs.toFixed(1) + ' hrs/day';
      document.getElementById('val-rota-wage').innerText = '+£' + wageTopup.toFixed(2) + '/hr';

      // Calculated impacts
      const walkoutReduction = Math.min(85, Math.round(hrs * 16));
      const recapturedSales = Math.round(hrs * 14600); // recaptured commuter orders
      const wageCost = Math.round(hrs * (13.0 + wageTopup) * 1.13 * 365);
      const grossMarginGained = recapturedSales * 0.72;
      const netProfitGain = Math.round(grossMarginGained - (wageTopup * hrs * 365));

      document.getElementById('rota-sim-walkout').innerText = '-' + walkoutReduction + '% Walkouts';
      document.getElementById('rota-sim-sales').innerText = '+£' + recapturedSales.toLocaleString() + ' / yr';
      document.getElementById('rota-sim-profit').innerText = '+£' + netProfitGain.toLocaleString() + ' / yr';
    }}

    // 7. Waste Management
    function renderWasteTab() {{
      const stores = [...currentData.stores].sort((a, b) => b.waste.cost_wasted - a.waste.cost_wasted);
      const tbody = document.getElementById('waste-tbody');
      tbody.innerHTML = '';

      stores.forEach(s => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{s.store_name}}</strong></td>
          <td class="text-right font-mono">${{s.waste.units_prepared.toLocaleString()}}</td>
          <td class="text-right font-mono text-rose">${{s.waste.units_wasted.toLocaleString()}}</td>
          <td class="text-right font-mono font-semibold">${{s.waste.waste_pct.toFixed(1)}}%</td>
          <td class="text-right font-mono font-semibold text-rose">£${{s.waste.cost_wasted.toLocaleString()}}</td>
        `;
        tbody.appendChild(tr);
      }});

      const ctx = document.getElementById('storeWasteChart');
      if (ctx) {{
        if (storeWasteChart) storeWasteChart.destroy();
        storeWasteChart = new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: stores.map(s => s.store_id),
            datasets: [{{
              label: 'Annual Cost of Food Wasted (£)',
              data: stores.map(s => s.waste.cost_wasted),
              backgroundColor: '#f59e0b',
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false
          }}
        }});
      }}
    }}

    // 8. Future Investments (£1.5M)
    function renderInvestmentsTab() {{
      const sites = currentData.candidate_sites;
      const tbody = document.getElementById('candidate-sites-tbody');
      tbody.innerHTML = '';

      sites.forEach(cs => {{
        const tr = document.createElement('tr');
        const isTrap = cs.site_id === 'CS7';
        const isWeak = cs.site_id === 'CS2';
        const recBadge = isTrap ? 'badge-rose' : (isWeak ? 'badge-amber' : 'badge-emerald');

        tr.innerHTML = `
          <td class="font-mono">${{cs.site_id}}</td>
          <td><strong>${{cs.site_name}}</strong></td>
          <td>${{cs.city}}</td>
          <td>${{cs.location_type}}</td>
          <td class="text-right font-mono">£${{cs.est_fitout_gbp.toLocaleString()}}</td>
          <td class="text-right font-mono">£${{cs.quoted_rent_gbp_month.toLocaleString()}}</td>
          <td class="text-right font-mono">${{cs.daily_footfall_street.toLocaleString()}}</td>
          <td class="text-right font-mono font-semibold ${{cs.projected_ebitda_gbp >= 0 ? 'text-emerald' : 'text-rose'}}">
            ${{cs.projected_ebitda_gbp < 0 ? '-' : ''}}£${{Math.abs(cs.projected_ebitda_gbp).toLocaleString()}}
          </td>
          <td class="text-right font-mono font-semibold">${{cs.payback_years}} yrs</td>
          <td style="font-size:0.75rem; color:${{isTrap ? 'var(--rose)' : 'var(--text-muted)'}};">${{cs.cannibalization_risk}}</td>
          <td><span class="badge ${{recBadge}}">${{cs.recommendation}}</span></td>
        `;
        tbody.appendChild(tr);
      }});

      renderBudgetPlanner();
    }}

    function renderBudgetPlanner() {{
      const plan = currentData.budget_plan.categories;
      const list = document.getElementById('budget-items-list');
      list.innerHTML = '';

      plan.forEach((item, idx) => {{
        const div = document.createElement('div');
        div.style.cssText = 'padding:0.75rem 1rem; background:var(--card-bg); border:1px solid var(--card-border); border-radius:10px; display:flex; align-items:center; justify-content:space-between;';
        div.innerHTML = `
          <label style="display:flex; align-items:center; gap:0.6rem; cursor:pointer; flex:1;">
            <input type="checkbox" id="budget-item-${{idx}}" checked onchange="calcBudgetPlan()">
            <div>
              <div style="font-weight:700; font-size:0.88rem;">${{item.name}}</div>
              <div style="font-size:0.75rem; color:var(--text-muted);">${{item.rationale}}</div>
            </div>
          </label>
          <div style="text-align:right; margin-left:1rem;">
            <div style="font-weight:800; font-mono; font-size:0.95rem;">£${{item.allocated_gbp.toLocaleString()}}</div>
            <div style="font-size:0.72rem; color:var(--emerald);">+£${{item.projected_annual_ebitda.toLocaleString()}}/yr</div>
          </div>
        `;
        list.appendChild(div);
      }});

      calcBudgetPlan();
    }}

    function calcBudgetPlan() {{
      const plan = currentData.budget_plan.categories;
      let spent = 0;
      let ebitda = 0;

      plan.forEach((item, idx) => {{
        const chk = document.getElementById(`budget-item-${{idx}}`);
        if (chk && chk.checked) {{
          spent += item.allocated_gbp;
          ebitda += item.projected_annual_ebitda;
        }}
      }});

      const totalBudget = 1500000;
      const remaining = totalBudget - spent;
      const payback = ebitda > 0 ? (spent / ebitda).toFixed(2) : 'N/A';

      document.getElementById('budget-spent-val').innerText = '£' + spent.toLocaleString() + ' / £' + totalBudget.toLocaleString();
      document.getElementById('budget-remaining-val').innerText = '£' + remaining.toLocaleString() + (remaining >= 0 ? ' Remaining' : ' Overbudget!');
      document.getElementById('budget-remaining-val').style.color = remaining >= 0 ? 'var(--emerald)' : 'var(--rose)';

      const pct = Math.min(100, Math.round((spent / totalBudget) * 100));
      const pBar = document.getElementById('budget-progress-bar');
      pBar.style.width = pct + '%';
      pBar.style.background = remaining >= 0 ? 'var(--emerald)' : 'var(--rose)';

      document.getElementById('budget-total-ebitda').innerText = '+£' + Math.round(ebitda).toLocaleString() + ' / yr';
      document.getElementById('budget-blended-payback').innerText = payback + ' Years';
    }}

    function resetRecommendedBudget() {{
      const plan = currentData.budget_plan.categories;
      plan.forEach((item, idx) => {{
        const chk = document.getElementById(`budget-item-${{idx}}`);
        if (chk) chk.checked = true;
      }});
      calcBudgetPlan();
    }}

    // 9. CEO AI Chatbot
    function askPredefined(question) {{
      document.getElementById('chatInput').value = question;
      sendChatMessage();
    }}

    async function sendChatMessage() {{
      const input = document.getElementById('chatInput');
      const text = input.value.trim();
      if (!text) return;

      const body = document.getElementById('chatBody');

      // User msg
      const userDiv = document.createElement('div');
      userDiv.className = 'chat-msg user';
      userDiv.innerText = text;
      body.appendChild(userDiv);
      input.value = '';
      body.scrollTop = body.scrollHeight;

      // Bot thinking
      const botDiv = document.createElement('div');
      botDiv.className = 'chat-msg bot';
      botDiv.innerHTML = '<em>Consulting Grind & Crumb intelligence data...</em>';
      body.appendChild(botDiv);
      body.scrollTop = body.scrollHeight;

      try {{
        // Call backend server api
        const res = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ prompt: text }})
        }});
        if (res.ok) {{
          const data = await res.json();
          // parse markdown simple
          botDiv.innerHTML = formatMarkdown(data.response);
        }} else {{
          botDiv.innerHTML = 'Error reaching assistant server. Please ensure server.py is running.';
        }}
      }} catch (err) {{
        // Fallback local response
        botDiv.innerHTML = formatMarkdown(getLocalFallbackAnswer(text));
      }}
      body.scrollTop = body.scrollHeight;
    }}

    function formatMarkdown(text) {{
      return text
        .replace(/### (.*)/g, '<div style="font-weight:700; font-size:1rem; margin-top:0.4rem; color:var(--accent);">$1</div>')
        .replace(/#### (.*)/g, '<div style="font-weight:700; font-size:0.9rem; margin-top:0.3rem;">$1</div>')
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
        .replace(/- (.*)/g, '<li>$1</li>')
        .split('\\n\\n').join('<br><br>');
    }}

    function getLocalFallbackAnswer(prompt) {{
      const p = prompt.toLowerCase();
      if (p.includes('piccadilly') || p.includes('s07')) {{
        return `### Manchester Piccadilly (S07) Analysis & Recovery Plan\\n\\n**Current Status:** **UNDERPERFORMING / HIGHEST LOSS IN CHAIN**\\n- **Sales:** £1,110,644 (Rank #1 in revenue chainwide)\\n- **Net Profit / Loss:** **-£49,697 (-4.5% margin)**\\n- **Annual Rent:** £366,000 (£30,500/month — 33% of total revenue!)\\n- **Labour Cost:** £295,690\\n- **Delivery Commission & Packaging:** £70,220\\n- **Staff Turnover:** **220%** (53 leavers on a headcount of 24, avg survey score 4.96/10)\\n\\n#### Root Causes:\\n1. **The £366k Rent Trap:** Rent of £30.5k/mo at Piccadilly station concourse is draining all profitability. Ollie Brent believes "we are the biggest so we are the most profitable, rent is head office's problem."\\n2. **Lunch Rush Friction & Walkouts:** Commuters between 12:00-13:00 abandon queues when more than 5 people deep. Baristas report only 3 staff on till/coffee during peak lunch when 5 are required.\\n3. **Delivery Disruptions:** Delivery tablets constantly ping for single americanos (£3.50), pulling baristas away from high-value physical customers waiting at the till.\\n4. **Relentless Barista Churn:** Baristas leave for neighbouring station concourse outlets paying £0.50/hr more.\\n\\n#### Actionable Strategic Plan:\\n1. **Renegotiate Transit Lease:** Open urgent discussions with Network Rail / landlord to convert fixed £30.5k/mo into a turnover-linked model (e.g., base £18k + 8% turnover).\\n2. **Install Separate Delivery Collection Hatch (£90k capex):** Decouple delivery drivers from physical commuters so baristas focus exclusively on station walk-ins.\\n3. **Add 2 Peak Lunch Staff:** Reallocate 4 hours daily to 11:30–13:30 to deploy 5 baristas on peak shift, recovering an estimated **+£65,000** in lost commuter walkouts.\\n4. **£0.50/hr Peak Transit Retention Bonus:** Implement a lunch retention wage supplement to stop the 220% turnover and avoid continuous recruitment costs.`;
      }}
      if (p.includes('trinity') || p.includes('s12') || p.includes('briggate') || p.includes('s03')) {{
        return `### Leeds Market Strategy: Leeds Briggate (S03) vs Leeds Trinity (S12)\\n\\n**Current Situation:**\\n- **Leeds Trinity (S12):** Opened September 2025 (£385k fitout capex). Annualized sales: £498,706, Profit: £24,961 (5.0% margin). Ramping up, but situated only 0.4 miles from Briggate.\\n- **Leeds Briggate (S03):** Flagship store. Sales dropped from ~£90k/month pre-September 2025 to ~£70k/month after Trinity opened (a 22% drop). Annual profit is £113,390 (12.9% margin).\\n- **Food Wastage Alert:** Briggate generated **£16,649 in food waste** (highest in the entire chain!). Store manager Grace Okafor kept central par levels unchanged despite lower footfall ("we bin more than we used to").\\n\\n#### Recommendations:\\n1. **Immediate Par Level Correction:** Cut Briggate’s daily bakery and lunch par prep by 18-20% to save **£6,000–£8,000** in annual food waste.\\n2. **Store Differentiation:**\\n   - **Briggate (Flagship, 56 seats):** Position as the premium, experiential, weekend brunch and artisan seating destination.\\n   - **Trinity (Standard, 40 seats):** Focus on fast office lunch grab-and-go and student app click & collect.\\n3. **Coordinated Par Planning:** Implement synchronized par-level forecasting across both Leeds sites so stock is distributed intelligently without double-prepping perishable items.`;
      }}
      if (p.includes('hull') || p.includes('s10')) {{
        return `### Hull Paragon (S10) Turnaround Diagnostics\\n\\n**Current Status:** **MIDDLE PERFORMING / AT-RISK**\\n- **Sales:** £540,486 | **Profit:** £47,842 (8.9% margin)\\n- **Waste Cost:** £16,303 (2nd highest waste in chain!)\\n- **Staff Turnover:** 26 leavers on 16 headcount (162% turnover), survey score 5.38/10.\\n\\n#### Core Issues:\\n1. **Safety-Buffer Over-Ordering:** Marcus Dyer intentionally over-orders pastries and sandwiches ("I'd rather bin it than disappoint someone"), directly burning £16.3k/year.\\n2. **Broken Equipment:** The boiler is ancient and the dishwasher broke 3 times this year, leading to £5,400+ in emergency repair invoices.\\n3. **Cleanliness & Morale Crisis:** Cleaner left in October and wasn't replaced. Baristas are scrubbing floors after hectic shifts, creating burnout and negative hygiene reviews.\\n\\n#### Recommendations:\\n1. **Cap Par Levels Dynamically:** Mandate automated footfall-based prep caps to eliminate Marcus’s manual over-ordering buffer (saves ~£7,000/yr).\\n2. **Boiler & Dishwasher Replacement (£15k capex):** Stop spending on recurring engineer callouts.\\n3. **Rehire Dedicated Cleaner:** Free up baristas to focus on speed and customer service, stabilizing staff morale.`;
      }}
      if (p.includes('1.5') || p.includes('budget') || p.includes('invest') || p.includes('candidate') || p.includes('allocation')) {{
        return `### £1.5M Capital Budget Allocation Strategy\\n\\nWe recommend dividing the **£1,500,000** capital budget across high-return new sites, critical store refits, operational bottleneck elimination, and digital tech:\\n\\n- **New Site: Manchester Oxford Road (CS3)**: **£240,000** (Payback: 1.2 yrs, EBITDA: +£192k/yr). 52,000 daily footfall, 31k students, lowest fitout in group.\\n- **New Site: York Railway Station (CS4)**: **£180,000** (Payback: 1.3 yrs, EBITDA: +£135k/yr). Proven transit kiosk model (like Sheffield Station S02).\\n- **New Site: Leeds Headingley (CS1)**: **£320,000** (Payback: 2.4 yrs, EBITDA: +£134k/yr). Vibrant student corridor 2.5m away. Zero cannibalization with Briggate/Trinity.\\n- **Flagship Refit: York Stonegate (S04)**: **£160,000** (Chain's top earner £192k profit; never refitted since 2019).\\n- **Piccadilly Delivery Hatch & Staff (S07)**: **£90,000** (Separate delivery riders; add 2 lunch staff).\\n- **Hull Paragon Infrastructure (S10)**: **£50,000** (Replace aging boiler & dishwasher; rehire cleaner).\\n- **Digital Upgrade: App v4.0 & Par AI**: **£160,000** (Reward recovery, 3pm markdowns, predictive par AI).\\n- **Staff Retention Fund**: **£100,000** (50p/hr lunch premium for transit baristas).\\n- **Contingency / Working Capital**: **£200,000**.\\n\\n⚠️ **CRITICAL WARNING — SITES TO REJECT:**\\n- **DO NOT INVEST IN Leeds Wellington Place (CS7):** High rent (£11.8k/mo), footfall only 9,500, extreme cannibalization of S03 & S12. Projected loss of -£82k/yr!\\n- **DO NOT INVEST IN Sheffield Kelham Island (CS2):** Fitout is £390k with low footfall (14.5k); payback is 25.3 years!`;
      }}
      if (p.includes('wellington')) {{
        return `### DO NOT OPEN Leeds Wellington Place (CS7)\\n\\nAnna Whitfield considered Wellington Place because 'Leeds has been good to us'. However, the data reveals Wellington Place is a **dangerous trap**:\\n- **Quoted Rent:** £11,800/month (£141,600/year)\\n- **Street Footfall:** Only 9,500/day\\n- **Cannibalization Risk:** Leeds ALREADY has Leeds Briggate (S03) and Leeds Trinity (S12) within 0.5 miles. Trinity already took 22% of Briggate's sales!\\n- **Financial Projection:** Projected **Loss of -£82,414/year** with a 99-year payback!\\n\\n**Verdict:** Completely reject CS7. If expanding in Leeds, choose **Headingley (CS1)** instead (suburban student hub 2.5 miles away with zero cannibalization).`;
      }}
      if (p.includes('delivery') || p.includes('partner') || p.includes('rusheats') || p.includes('dashly')) {{
        return `### Delivery Operations & Profitability Strategy\\n\\n- **Revenue:** £1,524,424 (17.6% of chain revenue).\\n- **Partner Split:** RushEats 62.4% (30% commission) | Dashly 37.6% (commission increased from 27% to 33% on April 1, 2026).\\n- **The Under-£8 Problem:** **29.0% of all delivery orders are under £8!** On a £5.00 order, after commission (£1.50), packaging (£0.45), food cost (£1.37), and 4 minutes of staff time (£0.87), net profit is negligible and loses money once rent is counted.\\n\\n**Recommendations:**\\n1. Implement £8 minimum order basket or £1.50 small-order surcharge.\\n2. Renegotiate Dashly 33% commission back to 28% under threat of shifting volume to RushEats.\\n3. Throttle single-coffee delivery orders during peak 12:00-13:00 lunch in transit stores.`;
      }}
      if (p.includes('waste')) {{
        return `### Food Waste Management Review (£133,815 Lost Annually)\\n\\n- **Bakery:** 52,652 units wasted (11.7% waste rate) — **£52,367 lost**\\n- **Lunch (Sandwiches/Salads):** 29,148 units wasted (8.8% waste rate) — **£68,162 lost** (highest cost!)\\n- **Breakfast:** 7,899 units wasted (6.7% waste rate) — **£13,286 lost**\\n\\n**Worst Stores:** Leeds Briggate (£16.6k), Hull Paragon (£16.3k), Manchester Piccadilly (£16.1k).\\n\\n**Actionable Solutions:**\\n1. **Dynamic Par-Level AI:** Shift from static central par levels to dynamic forecasting based on 3-day weather and footfall (saves ~£40k/yr).\\n2. **App 3pm 'Happy Hour' Markdowns:** 40% discount on unsold bakery goods after 15:00.\\n3. **Too Good To Go Surprise Bags:** Sell surplus lunch packs at £3.50.`;
      }}
      if (p.includes('oat') || p.includes('milk')) {{
        return `### The £0.40 Oat Milk Surcharge Backlash\\n\\n- Introduced 12 Jan 2026 to recover £40k/yr in ingredient cost.\\n- Two days later, rival **Bean Social scrapped their 45p plant milk surcharge** across all 40 northern sites.\\n- Generated 230+ customer complaints and visible loyalty visit declines.\\n- **Recommendation:** **Scrap the £0.40 surcharge immediately.** The customer churn far exceeds the £40k paper revenue. Offset ingredient costs with high-margin iced beverage combos.`;
      }}
      return `### Grind & Crumb Executive Summary\\n\\nGrind & Crumb operates 12 stores across Northern England generating **£8.66M in revenue** and **£1.07M in net operating profit (12.3% margin)**.\\n\\n**Key Priorities:**\\n1. Fix Manchester Piccadilly (S07) £366k rent trap and lunch bottleneck (-£49.7k loss).\\n2. Cut Leeds Briggate (S03) food waste by 20% to adjust for Leeds Trinity (S12) cannibalization.\\n3. Enforce £8 delivery minimum to eliminate losses on 29% of delivery orders.\\n4. Deploy the £1.5M budget into CS3 Manchester Oxford Rd, CS4 York Station Kiosk, CS1 Leeds Headingley, and York refit. Reject CS7 Wellington Place!`;
    }}

    // 10. File Upload Handling
    async function handleFileUpload(e) {{
      const file = e.target.files[0];
      if (!file) return;

      const status = document.getElementById('upload-status');
      status.style.display = 'block';
      status.innerHTML = `<div class="badge badge-blue">Uploading and processing ${{file.name}}...</div>`;

      const reader = new FileReader();
      reader.onload = async function(evt) {{
        const content = evt.target.result;
        try {{
          const res = await fetch('/api/upload', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ fileName: file.name, content: content }})
          }});
          if (res.ok) {{
            const resData = await res.json();
            currentData = resData.data;
            status.innerHTML = `<div class="badge badge-emerald" style="padding:0.5rem 1rem;">Successfully processed ${{file.name}}! All metrics and graphs updated.</div>`;
            initDashboard();
          }} else {{
            status.innerHTML = `<div class="badge badge-rose">Upload succeeded locally. Refresh dashboard to see changes.</div>`;
          }}
        }} catch (err) {{
          status.innerHTML = `<div class="badge badge-rose">Note: Running in standalone mode. To persist uploads to disk, ensure python server.py is running.</div>`;
        }}
      }};
      reader.readAsText(file);
    }}

    // Init All
    function initDashboard() {{
      renderOverviewTable();
      renderOverviewCharts();
      populateStoreSelector();
      renderStoreDeepDive();
      renderCostsTab();
      renderIncomeTab();
      renderDeliveryTab();
      renderStaffTab();
      renderWasteTab();
      renderInvestmentsTab();
    }}

    window.addEventListener('DOMContentLoaded', initDashboard);
  </script>
</body>
</html>
'''

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully built index.html!")

build_html()
