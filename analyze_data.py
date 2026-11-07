import csv
from collections import defaultdict
from datetime import datetime

def analyze():
    # 1. Stores metadata
    stores = {}
    with open('grind_and_crumb_data/stores.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            stores[r['store_id']] = r

    # 2. Daily sales
    daily_sales = defaultdict(lambda: defaultdict(lambda: {'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0, 'rec_in': 0, 'rec_app': 0, 'rec_del': 0}))
    store_annual_sales = defaultdict(lambda: {'instore': 0.0, 'app': 0.0, 'delivery': 0.0, 'total': 0.0, 'rec_in': 0, 'rec_app': 0, 'rec_del': 0})
    
    with open('grind_and_crumb_data/daily_store_sales.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            m = r['date'][:7]
            si = float(r['net_sales_instore_gbp'])
            sa = float(r['net_sales_app_gbp'])
            sd = float(r['net_sales_delivery_gbp'])
            tot = si + sa + sd
            ri = int(r['receipts_instore'])
            ra = int(r['receipts_app'])
            rd = int(r['receipts_delivery'])

            daily_sales[s][m]['instore'] += si
            daily_sales[s][m]['app'] += sa
            daily_sales[s][m]['delivery'] += sd
            daily_sales[s][m]['total'] += tot
            daily_sales[s][m]['rec_in'] += ri
            daily_sales[s][m]['rec_app'] += ra
            daily_sales[s][m]['rec_del'] += rd

            store_annual_sales[s]['instore'] += si
            store_annual_sales[s]['app'] += sa
            store_annual_sales[s]['delivery'] += sd
            store_annual_sales[s]['total'] += tot
            store_annual_sales[s]['rec_in'] += ri
            store_annual_sales[s]['rec_app'] += ra
            store_annual_sales[s]['rec_del'] += rd

    # 3. Monthly store costs
    store_costs = defaultdict(lambda: defaultdict(lambda: {'rent': 0.0, 'rates': 0.0, 'utilities': 0.0, 'repairs': 0.0, 'other_opex': 0.0, 'total': 0.0}))
    store_annual_costs = defaultdict(lambda: {'rent': 0.0, 'rates': 0.0, 'utilities': 0.0, 'repairs': 0.0, 'other_opex': 0.0, 'total': 0.0})
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

            store_costs[s][m]['rent'] += rnt
            store_costs[s][m]['rates'] += rat
            store_costs[s][m]['utilities'] += ut
            store_costs[s][m]['repairs'] += rep
            store_costs[s][m]['other_opex'] += op
            store_costs[s][m]['total'] += tot

            store_annual_costs[s]['rent'] += rnt
            store_annual_costs[s]['rates'] += rat
            store_annual_costs[s]['utilities'] += ut
            store_annual_costs[s]['repairs'] += rep
            store_annual_costs[s]['other_opex'] += op
            store_annual_costs[s]['total'] += tot

    # 4. Weekly labour costs
    store_monthly_labour = defaultdict(lambda: defaultdict(float))
    store_annual_labour = defaultdict(float)
    with open('grind_and_crumb_data/staff_rota_weekly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            m = r['week_start'][:7]
            h = float(r['scheduled_hours'])
            w = float(r['avg_hourly_wage_gbp'])
            lab = h * w * 1.13
            store_monthly_labour[s][m] += lab
            store_annual_labour[s] += lab

    # 5. Waste log
    waste_by_store_cat = defaultdict(lambda: defaultdict(lambda: {'prepared': 0, 'wasted': 0, 'cost': 0.0}))
    store_annual_waste = defaultdict(lambda: {'prepared': 0, 'wasted': 0, 'cost': 0.0})
    with open('grind_and_crumb_data/waste_log.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            cat = r['category']
            prep = float(r['units_prepared']) if r['units_prepared'] else 0.0
            wast = float(r['units_wasted']) if r['units_wasted'] else 0.0
            cost = float(r['est_cost_wasted_gbp']) if r['est_cost_wasted_gbp'] else 0.0
            waste_by_store_cat[s][cat]['prepared'] += prep
            waste_by_store_cat[s][cat]['wasted'] += wast
            waste_by_store_cat[s][cat]['cost'] += cost

            store_annual_waste[s]['prepared'] += prep
            store_annual_waste[s]['wasted'] += wast
            store_annual_waste[s]['cost'] += cost

    # 6. Delivery partner share in sample
    # Check transactions
    del_orders_by_partner = defaultdict(lambda: defaultdict(int))
    with open('grind_and_crumb_data/transactions.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['channel'] == 'Delivery':
                s = r['store_id']
                p = r['delivery_partner']
                del_orders_by_partner[s][p] += 1

    print("=== ANNUAL STORE P&L ===")
    months = sorted(list(store_costs['S01'].keys()))
    
    results = []
    for sid in sorted(stores.keys()):
        st_name = stores[sid]['store_name']
        sales = store_annual_sales[sid]['total']
        labour = store_annual_labour[sid]
        fixed = store_annual_costs[sid]['total']
        cogs = sales * 0.2741 # from product line ratio
        # Delivery costs:
        del_sales = store_annual_sales[sid]['delivery']
        del_orders = store_annual_sales[sid]['rec_del']
        # Partner proportion:
        total_p_sample = sum(del_orders_by_partner[sid].values())
        rusheats_share = del_orders_by_partner[sid]['RushEats'] / total_p_sample if total_p_sample else 0.5
        dashly_share = del_orders_by_partner[sid]['Dashly'] / total_p_sample if total_p_sample else 0.5
        # weighted commission: RushEats 30%, Dashly 27% (9 mos) & 33% (3 mos) -> avg 28.5%
        avg_comm = (rusheats_share * 0.30) + (dashly_share * 0.285)
        comm_cost = del_sales * avg_comm
        pack_cost = del_orders * 0.45
        del_total_cost = comm_cost + pack_cost
        
        total_cost = labour + fixed + cogs + del_total_cost
        profit = sales - total_cost
        margin = (profit / sales) * 100 if sales else 0.0

        results.append({
            'sid': sid,
            'name': st_name,
            'sales': sales,
            'labour': labour,
            'fixed': fixed,
            'rent': store_annual_costs[sid]['rent'],
            'rates': store_annual_costs[sid]['rates'],
            'utilities': store_annual_costs[sid]['utilities'],
            'repairs': store_annual_costs[sid]['repairs'],
            'other_opex': store_annual_costs[sid]['other_opex'],
            'cogs': cogs,
            'del_cost': del_total_cost,
            'waste_cost': store_annual_waste[sid]['cost'],
            'profit': profit,
            'margin': margin
        })

    # Sort by profit
    results.sort(key=lambda x: x['profit'], reverse=True)
    for r in results:
        print(f"{r['sid']} | {r['name']:<28} | Sales: £{r['sales']:>10,.0f} | Profit: £{r['profit']:>8,.0f} | Margin: {r['margin']:>5.1f}% | Rent: £{r['rent']:>7,.0f} | Waste: £{r['waste_cost']:>6,.0f}")

    print("\n=== MONTHLY PROFIT SPREAD FOR LEEDS BRIGGATE (S03) vs LEEDS TRINITY (S12) ===")
    for m in sorted(daily_sales['S03'].keys()):
        s03_s = daily_sales['S03'][m]['total']
        s12_s = daily_sales['S12'][m]['total']
        print(f"{m} -> S03 Briggate Sales: £{s03_s:,.0f} | S12 Trinity Sales: £{s12_s:,.0f}")

    print("\n=== WASTE BREAKDOWN CHAINWIDE ===")
    cat_waste = defaultdict(lambda: {'prep': 0, 'wasted': 0, 'cost': 0.0})
    for s in waste_by_store_cat:
        for c in waste_by_store_cat[s]:
            cat_waste[c]['prep'] += waste_by_store_cat[s][c]['prepared']
            cat_waste[c]['wasted'] += waste_by_store_cat[s][c]['wasted']
            cat_waste[c]['cost'] += waste_by_store_cat[s][c]['cost']
    for c, d in cat_waste.items():
        w_pct = (d['wasted'] / d['prep']) * 100 if d['prep'] else 0
        print(f"Category: {c:<10} | Prepared: {d['prep']:>8,.0f} | Wasted: {d['wasted']:>8,.0f} ({w_pct:>5.1f}%) | Cost Wasted: £{d['cost']:>8,.2f}")

analyze()
