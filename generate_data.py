import csv, json
from collections import defaultdict

def generate_consolidated_data():
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

    # 2. Daily Sales
    store_sales = defaultdict(lambda: {
        'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0,
        'orders_in': 0, 'orders_app': 0, 'orders_del': 0, 'orders_total': 0
    })
    monthly_sales = defaultdict(lambda: defaultdict(lambda: {'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0}))
    
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

    # 3. Monthly Store Costs
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

    # 4. Labour Costs
    store_labour = defaultdict(lambda: {'hours': 0.0, 'cost': 0.0})
    monthly_labour = defaultdict(lambda: defaultdict(float))
    daypart_labour = defaultdict(lambda: defaultdict(float))
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
            daypart_labour[s][dp] += h

    # 5. Waste Log
    waste_by_cat = defaultdict(lambda: defaultdict(lambda: {'prep': 0.0, 'wasted': 0.0, 'cost': 0.0}))
    store_waste = defaultdict(lambda: {'prep': 0.0, 'wasted': 0.0, 'cost': 0.0})
    with open('grind_and_crumb_data/waste_log.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            cat = r['category']
            prep = float(r['units_prepared']) if r['units_prepared'] else 0.0
            wast = float(r['units_wasted']) if r['units_wasted'] else 0.0
            cost = float(r['est_cost_wasted_gbp']) if r['est_cost_wasted_gbp'] else 0.0

            waste_by_cat[s][cat]['prep'] += prep
            waste_by_cat[s][cat]['wasted'] += wast
            waste_by_cat[s][cat]['cost'] += cost

            store_waste[s]['prep'] += prep
            store_waste[s]['wasted'] += wast
            store_waste[s]['cost'] += cost

    # 6. Staff Monthly
    staff_stats = defaultdict(lambda: {'headcount': 0, 'leavers': 0, 'starters': 0, 'survey_scores': []})
    with open('grind_and_crumb_data/staff_monthly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            staff_stats[s]['headcount'] = int(r['headcount']) # last month headcount
            staff_stats[s]['leavers'] += int(r['leavers'])
            staff_stats[s]['starters'] += int(r['new_starters'])
            staff_stats[s]['survey_scores'].append(float(r['staff_survey_score_10']))

    # 7. Customer Reviews & Ratings
    store_name_to_id = {v['store_name'].lower(): k for k, v in stores.items()}
    # raw store names mapping
    store_reviews = defaultdict(lambda: {'count': 0, 'sum_rating': 0.0, 'ratings': [0,0,0,0,0,0], 'complaints': defaultdict(int)})
    with open('grind_and_crumb_data/customer_reviews.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            raw_name = r['store_name_raw'].lower().strip()
            matched_id = None
            for sname, sid in store_name_to_id.items():
                if sname in raw_name or raw_name in sname:
                    matched_id = sid
                    break
            if not matched_id:
                # heuristic match
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
                txt = r['review_text'].lower()
                if 'oat' in txt: store_reviews[matched_id]['complaints']['oat_milk'] += 1
                if 'app' in txt or 'stamp' in txt: store_reviews[matched_id]['complaints']['app_issue'] += 1
                if 'queue' in txt or 'slow' in txt or 'wait' in txt: store_reviews[matched_id]['complaints']['wait_time'] += 1
                if 'clean' in txt or 'dirty' in txt: store_reviews[matched_id]['complaints']['cleanliness'] += 1
                if 'cold' in txt or 'stale' in txt or 'wrong' in txt: store_reviews[matched_id]['complaints']['quality'] += 1

    # 8. Footfall
    store_footfall = defaultdict(int)
    with open('grind_and_crumb_data/footfall.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            store_footfall[r['store_id']] += int(r['door_count'])

    # 9. Products & Line details
    products = {}
    with open('grind_and_crumb_data/products.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            products[r['product_id']] = {
                'id': r['product_id'],
                'name': r['product_name'],
                'category': r['category'],
                'menu_price': float(r['menu_price_gbp']),
                'cost': float(r['unit_cost_gbp']),
                'delivery_price': float(r['delivery_price_gbp']),
                'margin_gbp': float(r['menu_price_gbp']) - float(r['unit_cost_gbp']),
                'margin_pct': round((float(r['menu_price_gbp']) - float(r['unit_cost_gbp'])) / float(r['menu_price_gbp']) * 100, 1)
            }

    # 10. Partner Delivery info
    partner_stats = defaultdict(lambda: {'count': 0, 'sales': 0.0, 'stores': defaultdict(int)})
    with open('grind_and_crumb_data/transactions.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['channel'] == 'Delivery':
                p = r['delivery_partner']
                partner_stats[p]['count'] += 1
                partner_stats[p]['sales'] += float(r['net_gbp'])
                partner_stats[p]['stores'][r['store_id']] += 1

    # 11. Compile Store Summary
    all_stores_data = []
    chain_totals = defaultdict(float)

    months_list = ['2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']

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
        cogs = total_sales * 0.2741 # COGS ingredients
        labour_cost = s_labour['cost']
        rent = s_costs['rent']
        rates = s_costs['rates']
        utilities = s_costs['utilities']
        repairs = s_costs['repairs']
        other_opex = s_costs['other_opex']
        fixed_costs = s_costs['total']

        # Delivery cost calculation:
        # RushEats (30%), Dashly (28.5% avg over year)
        # Ratio of RushEats vs Dashly in sample:
        re_count = partner_stats['RushEats']['stores'].get(sid, 0)
        da_count = partner_stats['Dashly']['stores'].get(sid, 0)
        tot_del_sample = re_count + da_count
        re_share = re_count / tot_del_sample if tot_del_sample else 0.6
        da_share = da_count / tot_del_sample if tot_del_sample else 0.4
        comm_rate = (re_share * 0.30) + (da_share * 0.285)
        
        del_comm_cost = s_sales['delivery'] * comm_rate
        del_pack_cost = s_sales['orders_del'] * 0.45
        total_delivery_cost = del_comm_cost + del_pack_cost

        total_expenses = labour_cost + fixed_costs + cogs + total_delivery_cost
        net_profit = total_sales - total_expenses
        profit_margin = (net_profit / total_sales * 100) if total_sales > 0 else 0.0

        # Performance categorization:
        # Well performing: Profit Margin >= 15% AND Net Profit > £100k
        # Middle performing: Profit Margin between 7% and 15% AND Net Profit >= £40k
        # Underperforming: Profit Margin < 7% OR Net Profit < £40k (or negative profit!)
        if profit_margin >= 16.0:
            status = 'Performing Well'
            status_color = 'emerald'
        elif profit_margin >= 8.0:
            status = 'Middle Performing'
            status_color = 'amber'
        else:
            status = 'Underperforming'
            status_color = 'rose'

        # Monthly profit trend:
        store_monthly_trend = []
        for m in months_list:
            m_s = monthly_sales[sid][m]['total']
            m_fixed = monthly_costs[sid][m]['total']
            m_labour = monthly_labour[sid][m]
            m_cogs = m_s * 0.2741
            m_del_s = monthly_sales[sid][m]['delivery']
            m_del_orders = s_sales['orders_del'] / 12.0 # approx
            m_del_cost = (m_del_s * comm_rate) + (m_del_orders * 0.45)
            m_exp = m_fixed + m_labour + m_cogs + m_del_cost
            m_prof = m_s - m_exp
            store_monthly_trend.append({
                'month': m,
                'sales': round(m_s, 2),
                'expenses': round(m_exp, 2),
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
                'rent': round(rent, 2),
                'rates': round(rates, 2),
                'utilities': round(utilities, 2),
                'repairs': round(repairs, 2),
                'other_opex': round(other_opex, 2),
                'fixed_total': round(fixed_costs, 2),
                'cogs_ingredients': round(cogs, 2),
                'delivery_commission': round(del_comm_cost, 2),
                'delivery_packaging': round(del_pack_cost, 2),
                'delivery_total': round(total_delivery_cost, 2),
                'total_expenses': round(total_expenses, 2)
            },
            'profit': round(net_profit, 2),
            'margin': round(profit_margin, 2),
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
                'daypart_hours': dict(daypart_labour[sid])
            },
            'customer': {
                'review_count': s_reviews['count'],
                'avg_rating': avg_rev,
                'rating_counts': s_reviews['ratings'],
                'complaints': dict(s_reviews['complaints'])
            },
            'footfall': {
                'annual_door_count': s_foot,
                'conversion_rate_pct': round((s_sales['orders_in'] / s_foot * 100) if s_foot else 0, 1)
            },
            'monthly_trend': store_monthly_trend
        }
        all_stores_data.append(store_obj)

    # Chain totals
    chain_summary = {
        'total_revenue': sum(s['sales']['total'] for s in all_stores_data),
        'instore_revenue': sum(s['sales']['instore'] for s in all_stores_data),
        'app_revenue': sum(s['sales']['app'] for s in all_stores_data),
        'delivery_revenue': sum(s['sales']['delivery'] for s in all_stores_data),
        'total_labour': sum(s['costs']['labour'] for s in all_stores_data),
        'total_rent': sum(s['costs']['rent'] for s in all_stores_data),
        'total_rates': sum(s['costs']['rates'] for s in all_stores_data),
        'total_utilities': sum(s['costs']['utilities'] for s in all_stores_data),
        'total_repairs': sum(s['costs']['repairs'] for s in all_stores_data),
        'total_other_opex': sum(s['costs']['other_opex'] for s in all_stores_data),
        'total_cogs': sum(s['costs']['cogs_ingredients'] for s in all_stores_data),
        'total_delivery_commission': sum(s['costs']['delivery_commission'] for s in all_stores_data),
        'total_delivery_packaging': sum(s['costs']['delivery_packaging'] for s in all_stores_data),
        'total_delivery_costs': sum(s['costs']['delivery_total'] for s in all_stores_data),
        'total_expenses': sum(s['costs']['total_expenses'] for s in all_stores_data),
        'total_profit': sum(s['profit'] for s in all_stores_data),
        'overall_margin': round(sum(s['profit'] for s in all_stores_data) / sum(s['sales']['total'] for s in all_stores_data) * 100, 2),
        'total_waste_cost': sum(s['waste']['cost_wasted'] for s in all_stores_data),
        'total_orders': sum(s['orders']['total'] for s in all_stores_data),
        'store_count': len(all_stores_data)
    }

    # Save to JSON
    with open('grind_and_crumb_data/dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump({'chain': chain_summary, 'stores': all_stores_data, 'products': list(products.values())}, f, indent=2)

    print("Successfully generated dashboard_data.json!")
    print(f"Total chain revenue: £{chain_summary['total_revenue']:,.2f}")
    print(f"Total chain expenses: £{chain_summary['total_expenses']:,.2f}")
    print(f"Total chain profit: £{chain_summary['total_profit']:,.2f} ({chain_summary['overall_margin']}%)")

generate_consolidated_data()
