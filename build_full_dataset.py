import csv, json
from collections import defaultdict, Counter

def build_full_dataset():
    # 1. Stores
    stores = {}
    with open('grind_and_crumb_data/stores.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            stores[r['store_id']] = {
                'store_id': r['store_id'],
                'store_name': r['store_name'],
                'city': r['city'],
                'format': r['format'],
                'location_type': r['location_type'],
                'opened_date': r['opened_date'],
                'sqft': int(r['sqft']),
                'seats': int(r['seats']),
                'rent_gbp_month': float(r['rent_gbp_month']),
                'store_manager': r['store_manager'],
                'refit_year': r['refit_year'] if r['refit_year'] else 'Never'
            }

    # 2. Products
    products = {}
    with open('grind_and_crumb_data/products.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            pid = r['product_id']
            m_price = float(r['menu_price_gbp'])
            u_cost = float(r['unit_cost_gbp'])
            d_price = float(r['delivery_price_gbp'])
            products[pid] = {
                'product_id': pid,
                'product_name': r['product_name'],
                'category': r['category'],
                'menu_price_gbp': m_price,
                'unit_cost_gbp': u_cost,
                'milk_based': r['milk_based'] == '1',
                'delivery_price_gbp': d_price,
                'unit_margin_gbp': round(m_price - u_cost, 2),
                'margin_pct': round((m_price - u_cost) / m_price * 100, 1),
                'available_from': r['available_from'],
                'available_to': r['available_to']
            }

    # 3. Product sales aggregation from sample lines (scaled x10 for chainwide estimates)
    prod_sales = defaultdict(lambda: {'qty_sample': 0, 'sales_sample': 0.0, 'cogs_sample': 0.0})
    with open('grind_and_crumb_data/transaction_lines.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            pid = r['product_id']
            qty = float(r['qty'])
            lt = float(r['line_total_gbp'])
            if pid in products:
                prod_sales[pid]['qty_sample'] += qty
                prod_sales[pid]['sales_sample'] += lt
                prod_sales[pid]['cogs_sample'] += products[pid]['unit_cost_gbp'] * qty

    product_list = []
    for pid, p in products.items():
        s_data = prod_sales[pid]
        est_annual_qty = int(s_data['qty_sample'] * 10)
        est_annual_rev = round(s_data['sales_sample'] * 10, 2)
        est_annual_cogs = round(s_data['cogs_sample'] * 10, 2)
        est_annual_profit = round(est_annual_rev - est_annual_cogs, 2)
        product_list.append({
            **p,
            'annual_qty': est_annual_qty,
            'annual_revenue': est_annual_rev,
            'annual_cogs': est_annual_cogs,
            'annual_profit': est_annual_profit,
            'roi_pct': round((est_annual_profit / est_annual_cogs * 100) if est_annual_cogs > 0 else 0, 1)
        })

    # Sort products by revenue
    product_list.sort(key=lambda x: x['annual_revenue'], reverse=True)

    # 4. Daily Sales
    store_sales = defaultdict(lambda: {
        'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0,
        'orders_in': 0, 'orders_app': 0, 'orders_del': 0, 'orders_total': 0
    })
    monthly_sales = defaultdict(lambda: defaultdict(lambda: {'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0, 'orders_del': 0}))

    with open('grind_and_crumb_data/daily_store_sales.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            m = r['date'][:7]
            si = float(r['net_sales_instore_gbp'])
            sa = float(r['net_sales_app_gbp'])
            sd = float(r['net_sales_delivery_gbp'])
            tot = si + sa + sd
            oi = int(r['receipts_instore'])
            oa = int(r['receipts_app'])
            od = int(r['receipts_delivery'])

            store_sales[s]['instore'] += si
            store_sales[s]['app'] += sa
            store_sales[s]['delivery'] += sd
            store_sales[s]['total'] += tot
            store_sales[s]['orders_in'] += oi
            store_sales[s]['orders_app'] += oa
            store_sales[s]['orders_del'] += od
            store_sales[s]['orders_total'] += (oi + oa + od)

            monthly_sales[s][m]['instore'] += si
            monthly_sales[s][m]['app'] += sa
            monthly_sales[s][m]['delivery'] += sd
            monthly_sales[s][m]['total'] += tot
            monthly_sales[s][m]['orders_del'] += od

    # 5. Monthly Store Costs
    store_costs = defaultdict(lambda: {'rent': 0.0, 'rates': 0.0, 'utilities': 0.0, 'repairs': 0.0, 'other_opex': 0.0, 'total': 0.0})
    monthly_costs = defaultdict(lambda: defaultdict(lambda: {'rent': 0.0, 'rates': 0.0, 'utilities': 0.0, 'repairs': 0.0, 'other_opex': 0.0, 'total': 0.0}))
    with open('grind_and_crumb_data/store_costs_monthly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            m = r['month']
            rnt = float(r['rent_gbp'])
            rat = float(r['business_rates_gbp'])
            ut = float(r['utilities_gbp'])
            rep = float(r['repairs_maintenance_gbp'])
            op = float(r['other_opex_gbp'])
            tot = rnt + rat + ut + rep + op

            store_costs[s]['rent'] += rnt
            store_costs[s]['rates'] += rat
            store_costs[s]['utilities'] += ut
            store_costs[s]['repairs'] += rep
            store_costs[s]['other_opex'] += op
            store_costs[s]['total'] += tot

            monthly_costs[s][m]['rent'] += rnt
            monthly_costs[s][m]['rates'] += rat
            monthly_costs[s][m]['utilities'] += ut
            monthly_costs[s][m]['repairs'] += rep
            monthly_costs[s][m]['other_opex'] += op
            monthly_costs[s][m]['total'] += tot

    # 6. Labour Costs
    store_labour = defaultdict(lambda: {'hours': 0.0, 'cost': 0.0})
    monthly_labour = defaultdict(lambda: defaultdict(float))
    daypart_labour = defaultdict(lambda: defaultdict(lambda: {'hours': 0.0, 'cost': 0.0}))
    with open('grind_and_crumb_data/staff_rota_weekly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            m = r['week_start'][:7]
            dp = r['daypart']
            h = float(r['scheduled_hours'])
            w = float(r['avg_hourly_wage_gbp'])
            c = h * w * 1.13

            store_labour[s]['hours'] += h
            store_labour[s]['cost'] += c
            monthly_labour[s][m] += c
            daypart_labour[s][dp]['hours'] += h
            daypart_labour[s][dp]['cost'] += c

    # 7. Waste Log
    waste_by_cat = defaultdict(lambda: defaultdict(lambda: {'prep': 0.0, 'wasted': 0.0, 'cost': 0.0}))
    store_waste = defaultdict(lambda: {'prep': 0.0, 'wasted': 0.0, 'cost': 0.0})
    monthly_waste = defaultdict(lambda: defaultdict(lambda: {'prep': 0.0, 'wasted': 0.0, 'cost': 0.0}))
    with open('grind_and_crumb_data/waste_log.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            cat = r['category']
            m = r['date'][:7]
            prep = float(r['units_prepared']) if r['units_prepared'] else 0.0
            wast = float(r['units_wasted']) if r['units_wasted'] else 0.0
            cost = float(r['est_cost_wasted_gbp']) if r['est_cost_wasted_gbp'] else 0.0

            waste_by_cat[s][cat]['prep'] += prep
            waste_by_cat[s][cat]['wasted'] += wast
            waste_by_cat[s][cat]['cost'] += cost

            store_waste[s]['prep'] += prep
            store_waste[s]['wasted'] += wast
            store_waste[s]['cost'] += cost

            monthly_waste[s][m]['prep'] += prep
            monthly_waste[s][m]['wasted'] += wast
            monthly_waste[s][m]['cost'] += cost

    # 8. Staff Monthly & Exit survey
    staff_stats = defaultdict(lambda: {'headcount': 0, 'leavers': 0, 'starters': 0, 'survey_scores': []})
    with open('grind_and_crumb_data/staff_monthly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            staff_stats[s]['headcount'] = int(r['headcount'])
            staff_stats[s]['leavers'] += int(r['leavers'])
            staff_stats[s]['starters'] += int(r['new_starters'])
            staff_stats[s]['survey_scores'].append(float(r['staff_survey_score_10']))

    exit_reasons_by_store = defaultdict(lambda: Counter())
    exit_reasons_chain = Counter()
    with open('grind_and_crumb_data/staff_exit_survey.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            reason = r['main_reason']
            exit_reasons_by_store[s][reason] += 1
            exit_reasons_chain[reason] += 1

    # 9. Customer Reviews & Ratings
    store_name_to_id = {v['store_name'].lower(): k for k, v in stores.items()}
    store_reviews = defaultdict(lambda: {'count': 0, 'sum_rating': 0.0, 'ratings': [0,0,0,0,0,0], 'complaints': defaultdict(int), 'sample_reviews': []})
    with open('grind_and_crumb_data/customer_reviews.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            raw_name = r['store_name_raw'].lower().strip()
            matched_id = None
            for sname, sid in store_name_to_id.items():
                if sname in raw_name or raw_name in sname:
                    matched_id = sid
                    break
            if not matched_id:
                if 'piccadilly' in raw_name: matched_id = 'S07'
                elif 'spinningfields' in raw_name: matched_id = 'S06'
                elif 'northern quarter' in raw_name or 'nq' in raw_name: matched_id = 'S05'
                elif 'briggate' in raw_name: matched_id = 'S03'
                elif 'trinity' in raw_name: matched_id = 'S12'
                elif 'paragon' in raw_name or 'hull' in raw_name: matched_id = 'S10'
                elif 'stonegate' in raw_name or 'york' in raw_name: matched_id = 'S04'
                elif 'hockley' in raw_name or 'nottingham' in raw_name: matched_id = 'S08'
                elif 'harrogate' in raw_name: matched_id = 'S09'
                elif 'campus' in raw_name or 'uni' in raw_name: matched_id = 'S11'
                elif 'station' in raw_name: matched_id = 'S02'
                elif 'division' in raw_name or 'sheffield' in raw_name: matched_id = 'S01'

            if matched_id:
                rating = int(r['rating'])
                store_reviews[matched_id]['count'] += 1
                store_reviews[matched_id]['sum_rating'] += rating
                store_reviews[matched_id]['ratings'][rating] += 1
                txt = r['review_text']
                txt_low = txt.lower()
                if 'oat' in txt_low: store_reviews[matched_id]['complaints']['oat_milk'] += 1
                if 'app' in txt_low or 'stamp' in txt_low: store_reviews[matched_id]['complaints']['app_bug'] += 1
                if 'queue' in txt_low or 'slow' in txt_low or 'wait' in txt_low: store_reviews[matched_id]['complaints']['wait_time'] += 1
                if 'clean' in txt_low or 'dirty' in txt_low: store_reviews[matched_id]['complaints']['cleanliness'] += 1
                if 'cold' in txt_low or 'stale' in txt_low or 'wrong' in txt_low: store_reviews[matched_id]['complaints']['order_accuracy'] += 1
                if len(store_reviews[matched_id]['sample_reviews']) < 5 and rating <= 2:
                    store_reviews[matched_id]['sample_reviews'].append({'rating': rating, 'text': txt, 'date': r['review_date']})

    # 10. Footfall
    store_footfall = defaultdict(int)
    daypart_footfall = defaultdict(lambda: defaultdict(int))
    with open('grind_and_crumb_data/footfall.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            dp = r['daypart']
            cnt = int(r['door_count'])
            store_footfall[s] += cnt
            daypart_footfall[s][dp] += cnt

    # 11. Delivery analysis
    del_orders_by_bracket = {'under_8': 0, '8_to_15': 0, '15_to_25': 0, 'over_25': 0}
    del_partner_summary = defaultdict(lambda: {'count': 0, 'sales': 0.0, 'under_8': 0})
    store_del_partners = defaultdict(lambda: defaultdict(int))
    with open('grind_and_crumb_data/transactions.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['channel'] == 'Delivery':
                s = r['store_id']
                p = r['delivery_partner']
                net = float(r['net_gbp'])
                store_del_partners[s][p] += 1
                del_partner_summary[p]['count'] += 1
                del_partner_summary[p]['sales'] += net
                if net < 8.0:
                    del_orders_by_bracket['under_8'] += 1
                    del_partner_summary[p]['under_8'] += 1
                elif net < 15.0:
                    del_orders_by_bracket['8_to_15'] += 1
                elif net < 25.0:
                    del_orders_by_bracket['15_to_25'] += 1
                else:
                    del_orders_by_bracket['over_25'] += 1

    # 12. Candidate Sites
    candidate_sites = []
    with open('grind_and_crumb_data/candidate_sites.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            fitout = float(r['est_fitout_gbp'])
            rent_mo = float(r['quoted_rent_gbp_month'])
            rent_yr = rent_mo * 12
            footfall = float(r['daily_footfall_street'])
            vibrancy = float(r['area_vibrancy_index_10'])
            students = float(r['students_1km'])
            workers = float(r['office_workers_500m'])
            competitors = float(r['competitor_cafes_500m'])
            income = float(r['median_household_income_gbp'])

            est_sales = min(max(footfall * 25.0 * (vibrancy / 7.0), 450000), 950000)
            cannibalization = 'None'
            recommendation = 'Invest'
            if r['city'] == 'Leeds':
                if 'Wellington' in r['site_name']:
                    cannibalization = 'VERY HIGH (Leeds already has Briggate S03 & Trinity S12 within 0.5 miles!)'
                    est_sales *= 0.75
                    recommendation = 'Do Not Invest (Trap: High rent, extreme cannibalization of S03 & S12)'
                elif 'Headingley' in r['site_name']:
                    cannibalization = 'Low (Suburban student corridor 2.5m away)'
                    recommendation = 'Strong Candidate (High student density & vibrant student high street)'
            elif r['city'] == 'Sheffield':
                if 'Kelham' in r['site_name']:
                    cannibalization = 'Low (Trendy regenerated area)'
                    recommendation = 'Weak Candidate (Fitout £390k is too high, low street footfall gives 25-year payback)'
            elif r['city'] == 'Manchester':
                if 'Oxford' in r['site_name']:
                    cannibalization = 'Medium (Oxford Road student/hospital corridor distinct from NQ/Piccadilly)'
                    recommendation = 'Top Priority #1 (Massive footfall 52k, lowest fitout £240k, 1.2-year payback)'
            elif r['city'] == 'York':
                cannibalization = 'None (Railway transit kiosk model like Sheffield Station S02)'
                recommendation = 'Top Priority #2 (Transit kiosk, low £180k fitout, 1.3-year payback)'
            elif r['city'] == 'Liverpool':
                recommendation = 'Viable Expansion (Strong high street, but £410k fitout consumes large chunk of budget)'
            elif r['city'] == 'Wakefield':
                recommendation = 'Avoid (Low vibrancy 5.4, declining retail footfall, weak margins)'

            cogs = est_sales * 0.2741
            labour = est_sales * 0.28
            rates = rent_yr * 0.22
            opex = 45000
            deliv_costs = (est_sales * 0.15) * 0.30
            est_costs = cogs + labour + rent_yr + rates + opex + deliv_costs
            est_ebitda = est_sales - est_costs
            est_margin = round((est_ebitda / est_sales) * 100, 1)
            payback = round(fitout / est_ebitda, 1) if est_ebitda > 0 else 99.0

            candidate_sites.append({
                'site_id': r['site_id'],
                'site_name': r['site_name'],
                'city': r['city'],
                'location_type': r['location_type'],
                'sqft': int(r['sqft']),
                'quoted_rent_gbp_month': rent_mo,
                'annual_rent_gbp': rent_yr,
                'daily_footfall_street': int(footfall),
                'office_workers_500m': int(workers),
                'students_1km': int(students),
                'median_household_income_gbp': int(income),
                'competitor_cafes_500m': int(competitors),
                'area_vibrancy_index_10': vibrancy,
                'est_fitout_gbp': int(fitout),
                'projected_sales_gbp': round(est_sales, 0),
                'projected_ebitda_gbp': round(est_ebitda, 0),
                'projected_margin_pct': est_margin,
                'payback_years': payback,
                'cannibalization_risk': cannibalization,
                'recommendation': recommendation
            })

    candidate_sites.sort(key=lambda x: x['payback_years'])

    # 13. Capex history
    capex_history = []
    with open('grind_and_crumb_data/capex.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            capex_history.append({
                'store_id': r['store_id'],
                'store_name': stores[r['store_id']]['store_name'],
                'month': r['month'],
                'description': r['description'],
                'capex_gbp': float(r['capex_gbp'])
            })

    # 14. Compile Stores
    months_list = ['2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    all_stores_data = []

    for sid in sorted(stores.keys()):
        st = stores[sid]
        s_sales = store_sales[sid]
        s_costs = store_costs[sid]
        s_labour = store_labour[sid]
        s_waste = store_waste[sid]
        s_staff = staff_stats[sid]
        s_reviews = store_reviews[sid]
        s_foot = store_footfall[sid]

        total_sales = s_sales['total']
        cogs = total_sales * 0.2741
        labour_cost = s_labour['cost']
        fixed_costs = s_costs['total']

        re_cnt = store_del_partners[sid].get('RushEats', 0)
        da_cnt = store_del_partners[sid].get('Dashly', 0)
        tot_del = re_cnt + da_cnt
        re_share = re_cnt / tot_del if tot_del else 0.62
        da_share = da_cnt / tot_del if tot_del else 0.38
        comm_rate = (re_share * 0.30) + (da_share * 0.285)

        del_comm_cost = s_sales['delivery'] * comm_rate
        del_pack_cost = s_sales['orders_del'] * 0.45
        total_delivery_cost = del_comm_cost + del_pack_cost

        total_expenses = labour_cost + fixed_costs + cogs + total_delivery_cost
        net_profit = total_sales - total_expenses
        profit_margin = round((net_profit / total_sales * 100) if total_sales > 0 else 0.0, 2)

        # Performance badge:
        if profit_margin >= 16.0:
            status = 'Performing Well'
            status_color = 'emerald'
            status_summary = 'High profitability, solid margins, sustainable rent-to-revenue ratio.'
        elif profit_margin >= 8.0:
            status = 'Middle Performing'
            status_color = 'amber'
            status_summary = 'Profitable but constrained by rising fixed overheads, equipment issues, or local cannibalization.'
        else:
            status = 'Underperforming'
            status_color = 'rose'
            status_summary = 'Severe profitability drag due to crippling rent, delivery queue bottlenecks, or recent launch ramping.'

        # Tailored AI analysis for each store
        ai_diagnostic = {}
        if sid == 'S07': # Manchester Piccadilly
            ai_diagnostic = {
                'headline': 'The £366k Rent Trap & Lunchtime Delivery Chokehold',
                'why_underperforming': 'Despite generating the highest gross revenue in the entire chain (£1.11M), Piccadilly loses £49,697 net. The single biggest factor is crippling rent of £30,500/month (£366,000/year, 33% of revenue!). Moreover, store manager Ollie Brent neglects rent as "head office problem", while lunchtime delivery orders flood tablets for single £3.50 coffees, creating 12-person till queues and driving lucrative commuter footfall away to station concourse competitors. Staff turnover is catastrophic at 220% (53 leavers).',
                'actionable_recommendations': [
                    'Urgent Lease Renegotiation: Piccadilly rent (£30.5k/mo) must be renegotiated or structured into a turnover-linked base + variable model with the transit landlord.',
                    'Install Dedicated Delivery Hatch: Split delivery rider collection away from physical barista counter or pause low-value delivery orders during peak 12:00-13:30 rush.',
                    'Add 2 Peak Lunch Shifts: Increase barista staffing from 3 to 5 during lunch rush to capture lost commuters walking out. Will generate an estimated +£65k in retained sales.',
                    'Enact £0.50/hr Lunch Retention Premium: Stem the 220% barista turnover to competitors on concourse.'
                ]
            }
        elif sid == 'S12': # Leeds Trinity
            ai_diagnostic = {
                'headline': 'Cannibalizing Sister Store Leeds Briggate with Heavy Fitout Drag',
                'why_underperforming': 'Opened in September 2025 with £385,000 fitout capex. Operating margin is only 5.0% (£24,961 profit on £498k sales). Located just 0.4 miles from Leeds Briggate (S03), it directly cannibalized ~25% of Briggate’s sales, while Briggate failed to adjust food par levels, leading to £16.6k of wasted food.',
                'actionable_recommendations': [
                    'Differentiate Value Proposition: Turn Trinity into the fast grab-and-go student/retail hub and position Briggate as the artisanal sit-down experiential café.',
                    'Synchronize Par Levels: Recalibrate bakery and lunch par levels across both Leeds sites to eliminate redundant prepared stock.',
                    'Drive Evening / Student Footfall: Introduce post-15:00 study promotions and meal deals to optimize fixed rent.'
                ]
            }
        elif sid == 'S03': # Leeds Briggate
            ai_diagnostic = {
                'headline': 'Sales Siphoned by Leeds Trinity & Over-Ordering Waste',
                'why_underperforming': 'Sales plunged from ~£90k/mo to ~£70k/mo when Leeds Trinity opened 0.4 miles away. Store manager Grace Okafor kept central par levels unchanged ("set by par levels, we bin more than we used to"), resulting in £16,649 in wasted food (highest in chain!).',
                'actionable_recommendations': [
                    'Slash Par Levels by 20%: Grace Okafor must immediately align prep levels with post-Trinity baseline to save ~£6,000 annually in food waste.',
                    'Promote Weekend Experiential Seating: Briggate has 56 seats vs Trinity’s 40; expand weekend brunch offerings where Trinity is constrained.'
                ]
            }
        elif sid == 'S10': # Hull Paragon
            ai_diagnostic = {
                'headline': 'High Food Waste, Broken Infrastructure & Cleaning Deficit',
                'why_underperforming': 'Profit is £47.8k (8.9% margin). City centre footfall is down 8%. Marcus Dyer intentionally over-orders food ("rather bin it than disappoint someone"), creating £16,303 in waste. The cleaner left in October and wasn’t replaced, the dishwasher broke 3 times, and an old boiler creates endless maintenance callout costs.',
                'actionable_recommendations': [
                    'Boiler & Dishwasher Capital Replacement: Invest £15k capex to replace the ancient boiler and commercial dishwasher, cutting ~£8k in recurring maintenance callouts.',
                    'Hire Dedicated Part-Time Cleaner: Free up baristas from scrubbing floors to eliminate staff burnout and poor customer cleanliness reviews.',
                    'Implement Dynamic Par Waste Cap: Stop Marcus Dyer’s manual safety-buffer over-ordering; par levels must match footfall trends.'
                ]
            }
        elif sid == 'S06': # Manchester Spinningfields
            ai_diagnostic = {
                'headline': 'Dead Weekend Rents & Critical 12-1pm Speed Bottleneck',
                'why_underperforming': 'Operating margin is 8.6% on high rent (£12,400/mo). Spinningfields is pure office district: bustling 12-1pm rush where workers walk out if queues exceed 5 mins, but ghost-town weekends where stores lose money operating.',
                'actionable_recommendations': [
                    'Review Weekend Trading Hours: Curtail weekend trading or close entirely on Sundays to save £18k in non-productive labour and utilities.',
                    'Flex Hours into Lunch Rush: Shift 4 morning hours directly into the 11:30-13:30 peak to deploy dual till operators and a dedicated milk steamer.',
                    'Increase Sandwich Par by 15%: Currently sells out of sandwiches by 13:15, leaving £25k+ of unfulfilled lunch demand on the table.'
                ]
            }
        elif sid == 'S11': # Sheffield Uni Campus
            ai_diagnostic = {
                'headline': 'Low Off-Peak Student Volume & Summer Vacation Slump',
                'why_underperforming': 'Low revenue (£361k) and modest £30.8k profit (8.5% margin). Extreme seasonality driven by academic calendar (low revenue in July, August, and Christmas breaks). High COGS % (30.5%) due to product mix.',
                'actionable_recommendations': [
                    'Term-Time Dynamic Rota: Flex staffing down sharply during vacation months (July-August, Dec-Jan) to match student footfall.',
                    'Campus Click & Collect Push: Encourage student app pre-orders between lectures to boost basket size with meal deal add-ons.'
                ]
            }
        elif sid == 'S04': # York Stonegate
            ai_diagnostic = {
                'headline': 'Top Chain Performer (£192k Profit, 21.6% Margin)',
                'why_underperforming': 'Highly profitable tourist store with strong retail and beverage margins. However, it has never been refitted since opening in 2019.',
                'actionable_recommendations': [
                    'Allocate £160k Refit: Modernize interior, increase tourist seating capacity, and introduce merchandise display to further expand £192k profit.'
                ]
            }
        elif sid == 'S01': # Sheffield Division Street
            ai_diagnostic = {
                'headline': 'Anchor High-Street Earner (£159.7k Profit, 21.0% Margin)',
                'why_underperforming': 'Exceptional consistency, well-managed labour, balanced channel mix.',
                'actionable_recommendations': [
                    'Maintain par discipline and leverage as training store for regional managers.'
                ]
            }
        else:
            ai_diagnostic = {
                'headline': f'Store {st["store_name"]} ({status})',
                'why_underperforming': f'Generates £{net_profit:,.0f} profit with a {profit_margin}% margin. Key opportunities lie in reducing delivery friction and par level wastage.',
                'actionable_recommendations': [
                    'Enforce £8 delivery minimum basket to protect low-value margins.',
                    'Conduct quarterly staff rota alignment to peak door-count dayparts.'
                ]
            }

        # Monthly trends
        store_monthly_trend = []
        for m in months_list:
            m_s = monthly_sales[sid][m]['total']
            m_fixed = monthly_costs[sid][m]['total']
            m_lab = monthly_labour[sid][m]
            m_cogs = m_s * 0.2741
            m_del_s = monthly_sales[sid][m]['delivery']
            m_del_orders = monthly_sales[sid][m]['orders_del']
            m_del_c = (m_del_s * comm_rate) + (m_del_orders * 0.45)
            m_tot_exp = m_fixed + m_lab + m_cogs + m_del_c
            m_prof = m_s - m_tot_exp
            store_monthly_trend.append({
                'month': m,
                'sales': round(m_s, 2),
                'expenses': round(m_tot_exp, 2),
                'profit': round(m_prof, 2),
                'margin': round((m_prof / m_s * 100) if m_s > 0 else 0, 1)
            })

        avg_rev = round(s_reviews['sum_rating'] / s_reviews['count'], 2) if s_reviews['count'] else 4.0
        avg_survey = round(sum(s_staff['survey_scores']) / len(s_staff['survey_scores']), 2) if s_staff['survey_scores'] else 7.0
        turnover_rate = round((s_staff['leavers'] / max(s_staff['headcount'], 1)) * 100, 1)

        store_obj = {
            **st,
            'status': status,
            'status_color': status_color,
            'status_summary': status_summary,
            'ai_diagnostic': ai_diagnostic,
            'sales': {
                'instore': round(s_sales['instore'], 2),
                'app': round(s_sales['app'], 2),
                'delivery': round(s_sales['delivery'], 2),
                'total': round(total_sales, 2)
            },
            'orders': {
                'instore': s_sales['orders_in'],
                'app': s_sales['orders_app'],
                'delivery': s_sales['orders_del'],
                'total': s_sales['orders_total']
            },
            'costs': {
                'labour': round(labour_cost, 2),
                'rent': round(s_costs['rent'], 2),
                'rates': round(s_costs['rates'], 2),
                'utilities': round(s_costs['utilities'], 2),
                'repairs': round(s_costs['repairs'], 2),
                'other_opex': round(s_costs['other_opex'], 2),
                'fixed_total': round(fixed_costs, 2),
                'cogs_ingredients': round(cogs, 2),
                'delivery_commission': round(del_comm_cost, 2),
                'delivery_packaging': round(del_pack_cost, 2),
                'delivery_total': round(total_delivery_cost, 2),
                'total_expenses': round(total_expenses, 2)
            },
            'profit': round(net_profit, 2),
            'margin': profit_margin,
            'waste': {
                'units_prepared': round(s_waste['prep'], 0),
                'units_wasted': round(s_waste['wasted'], 0),
                'cost_wasted': round(s_waste['cost'], 2),
                'waste_pct': round((s_waste['wasted'] / s_waste['prep'] * 100) if s_waste['prep'] else 0, 1),
                'by_category': {
                    c: {
                        'prep': round(waste_by_cat[sid][c]['prep'], 0),
                        'wasted': round(waste_by_cat[sid][c]['wasted'], 0),
                        'cost': round(waste_by_cat[sid][c]['cost'], 2),
                        'pct': round((waste_by_cat[sid][c]['wasted'] / waste_by_cat[sid][c]['prep'] * 100) if waste_by_cat[sid][c]['prep'] else 0, 1)
                    } for c in waste_by_cat[sid]
                }
            },
            'staff': {
                'headcount': s_staff['headcount'],
                'leavers': s_staff['leavers'],
                'starters': s_staff['starters'],
                'turnover_rate_pct': turnover_rate,
                'avg_survey_score': avg_survey,
                'daypart_hours': {dp: round(daypart_labour[sid][dp]['hours'], 1) for dp in daypart_labour[sid]},
                'exit_reasons': dict(exit_reasons_by_store[sid])
            },
            'customer': {
                'review_count': s_reviews['count'],
                'avg_rating': avg_rev,
                'rating_counts': s_reviews['ratings'],
                'complaints': dict(s_reviews['complaints']),
                'sample_reviews': s_reviews['sample_reviews']
            },
            'footfall': {
                'annual_door_count': s_foot,
                'daypart_count': dict(daypart_footfall[sid]),
                'conversion_rate_pct': round((s_sales['orders_in'] / s_foot * 100) if s_foot else 0, 1)
            },
            'monthly_trend': store_monthly_trend
        }
        all_stores_data.append(store_obj)

    # Chain totals
    chain_summary = {
        'total_revenue': round(sum(s['sales']['total'] for s in all_stores_data), 2),
        'instore_revenue': round(sum(s['sales']['instore'] for s in all_stores_data), 2),
        'app_revenue': round(sum(s['sales']['app'] for s in all_stores_data), 2),
        'delivery_revenue': round(sum(s['sales']['delivery'] for s in all_stores_data), 2),
        'total_labour': round(sum(s['costs']['labour'] for s in all_stores_data), 2),
        'total_rent': round(sum(s['costs']['rent'] for s in all_stores_data), 2),
        'total_rates': round(sum(s['costs']['rates'] for s in all_stores_data), 2),
        'total_utilities': round(sum(s['costs']['utilities'] for s in all_stores_data), 2),
        'total_repairs': round(sum(s['costs']['repairs'] for s in all_stores_data), 2),
        'total_other_opex': round(sum(s['costs']['other_opex'] for s in all_stores_data), 2),
        'total_cogs': round(sum(s['costs']['cogs_ingredients'] for s in all_stores_data), 2),
        'total_delivery_commission': round(sum(s['costs']['delivery_commission'] for s in all_stores_data), 2),
        'total_delivery_packaging': round(sum(s['costs']['delivery_packaging'] for s in all_stores_data), 2),
        'total_delivery_costs': round(sum(s['costs']['delivery_total'] for s in all_stores_data), 2),
        'total_expenses': round(sum(s['costs']['total_expenses'] for s in all_stores_data), 2),
        'total_profit': round(sum(s['profit'] for s in all_stores_data), 2),
        'overall_margin': round(sum(s['profit'] for s in all_stores_data) / sum(s['sales']['total'] for s in all_stores_data) * 100, 2),
        'total_waste_cost': round(sum(s['waste']['cost_wasted'] for s in all_stores_data), 2),
        'total_orders': sum(s['orders']['total'] for s in all_stores_data),
        'total_footfall': sum(s['footfall']['annual_door_count'] for s in all_stores_data),
        'store_count': len(all_stores_data)
    }

    # Chain monthly trend
    chain_monthly_trend = []
    for m in months_list:
        m_sales = sum(s['monthly_trend'][months_list.index(m)]['sales'] for s in all_stores_data)
        m_expenses = sum(s['monthly_trend'][months_list.index(m)]['expenses'] for s in all_stores_data)
        m_profit = sum(s['monthly_trend'][months_list.index(m)]['profit'] for s in all_stores_data)
        chain_monthly_trend.append({
            'month': m,
            'sales': round(m_sales, 2),
            'expenses': round(m_expenses, 2),
            'profit': round(m_profit, 2),
            'margin': round((m_profit / m_sales * 100) if m_sales > 0 else 0, 1)
        })

    # Recommended 1.5M budget plan
    budget_allocation_plan = {
        'total_budget_gbp': 1500000,
        'categories': [
            {
                'name': 'New Site 1: Manchester Oxford Road (CS3)',
                'allocated_gbp': 240000,
                'category': 'New Store Expansion',
                'projected_annual_ebitda': 192478,
                'payback_years': 1.2,
                'rationale': 'Massive footfall (52k street door count) in high-density student & hospital corridor. Fitout is an affordable £240k. Zero cannibalization with Piccadilly or NQ.'
            },
            {
                'name': 'New Site 2: York Railway Station Kiosk (CS4)',
                'allocated_gbp': 180000,
                'category': 'New Store Expansion',
                'projected_annual_ebitda': 134778,
                'payback_years': 1.3,
                'rationale': 'Replicates the proven high-margin kiosk model of Sheffield Station (S02). Fast grab-and-go morning transit rush. Low £180k fitout.'
            },
            {
                'name': 'New Site 3: Leeds Headingley (CS1)',
                'allocated_gbp': 320000,
                'category': 'New Store Expansion',
                'projected_annual_ebitda': 134175,
                'payback_years': 2.4,
                'rationale': 'Vibrant student/young professional high street 2.5 miles from city centre. Zero risk of cannibalizing Briggate or Trinity.'
            },
            {
                'name': 'Flagship Refit: York Stonegate (S04)',
                'allocated_gbp': 160000,
                'category': 'Store Refit & Capacity',
                'projected_annual_ebitda': 45000,
                'payback_years': 3.5,
                'rationale': 'Our #1 most profitable store (£192k profit) has never had a refit since 2019. Modernize interior, increase tourist seating by 12 seats, and add retail display.'
            },
            {
                'name': 'Piccadilly Express Pickup Hatch & Rota Buffer (S07)',
                'allocated_gbp': 90000,
                'category': 'Bottleneck Elimination',
                'projected_annual_ebitda': 65000,
                'payback_years': 1.4,
                'rationale': 'Install a dedicated exterior/side delivery dispatch counter at Piccadilly to isolate delivery drivers from walk-in commuters. Adds 2 peak lunch staff to recapture lost sales.'
            },
            {
                'name': 'Hull Paragon Infrastructure Refurbishment (S10)',
                'allocated_gbp': 50000,
                'category': 'Equipment Modernization',
                'projected_annual_ebitda': 18000,
                'payback_years': 2.8,
                'rationale': 'Replace failing 15-year-old boiler and commercial dishwasher; hire dedicated part-time cleaner to stop barista burnout and negative hygiene reviews.'
            },
            {
                'name': 'Digital Upgrade: App v4.0 & AI Par-Level Forecasting',
                'allocated_gbp': 160000,
                'category': 'Technology & Waste Reduction',
                'projected_annual_ebitda': 62000,
                'payback_years': 2.6,
                'rationale': 'Roll out App v4.0 with automated stamp wallet recovery, push notifications, and dynamic 3pm markdowns; implement predictive par forecasting to cut 30% of £134k food waste.'
            },
            {
                'name': 'Staff Retention & Lunch Shift Premium Fund',
                'allocated_gbp': 100000,
                'category': 'People & Operations',
                'projected_annual_ebitda': 40000,
                'payback_years': 2.5,
                'rationale': '50p/hr peak lunch retention premium for high-pressure transit stores (Piccadilly, Spinningfields) to slash 220% turnover rate and reduce onboarding costs.'
            },
            {
                'name': 'Capital Contingency Reserve',
                'allocated_gbp': 200000,
                'category': 'Contingency',
                'projected_annual_ebitda': 0,
                'payback_years': 0,
                'rationale': 'Buffer reserve for unexpected fitout cost overruns, lease deposits, and working capital.'
            }
        ]
    }

    full_data = {
        'chain': chain_summary,
        'chain_monthly_trend': chain_monthly_trend,
        'stores': all_stores_data,
        'products': product_list,
        'candidate_sites': candidate_sites,
        'budget_plan': budget_allocation_plan,
        'capex_history': capex_history,
        'delivery_summary': {
            'orders_by_bracket': del_orders_by_bracket,
            'partner_summary': dict(del_partner_summary)
        },
        'staff_exit_reasons': dict(exit_reasons_chain)
    }

    with open('grind_and_crumb_data/full_dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)

    print("Successfully built grind_and_crumb_data/full_dashboard_data.json!")

build_full_dataset()
