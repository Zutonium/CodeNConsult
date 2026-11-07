import csv
from collections import defaultdict, Counter

def deep_dive():
    # 1. Product ROI & Sales ranking (from sample transaction lines scaled up)
    products = {}
    with open('grind_and_crumb_data/products.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            products[r['product_id']] = {
                'id': r['product_id'],
                'name': r['product_name'],
                'category': r['category'],
                'price': float(r['menu_price_gbp']),
                'cost': float(r['unit_cost_gbp']),
                'del_price': float(r['delivery_price_gbp']),
                'margin_gbp': float(r['menu_price_gbp']) - float(r['unit_cost_gbp']),
                'margin_pct': (float(r['menu_price_gbp']) - float(r['unit_cost_gbp'])) / float(r['menu_price_gbp']) * 100
            }

    prod_sales = defaultdict(lambda: {'qty': 0, 'revenue': 0.0, 'cogs': 0.0})
    with open('grind_and_crumb_data/transaction_lines.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            pid = r['product_id']
            qty = float(r['qty'])
            tot = float(r['line_total_gbp'])
            if pid in products:
                prod_sales[pid]['qty'] += qty
                prod_sales[pid]['revenue'] += tot
                prod_sales[pid]['cogs'] += products[pid]['cost'] * qty

    print("=== TOP 5 PRODUCTS BY REVENUE (Sample x 10) ===")
    sorted_prods = sorted(prod_sales.items(), key=lambda x: x[1]['revenue'], reverse=True)
    for pid, d in sorted_prods[:5]:
        p = products[pid]
        print(f"{p['name']} ({p['category']}): Revenue=£{d['revenue']*10:,.0f}, Qty={d['qty']*10:,.0f}, Unit Margin={p['margin_pct']:.1f}%")

    print("\n=== BOTTOM 5 PRODUCTS BY REVENUE ===")
    for pid, d in sorted_prods[-5:]:
        p = products[pid]
        print(f"{p['name']} ({p['category']}): Revenue=£{d['revenue']*10:,.0f}, Qty={d['qty']*10:,.0f}, Unit Margin={p['margin_pct']:.1f}%")

    # 2. Staff Turnover and Surveys
    staff_monthly = defaultdict(lambda: {'headcount': 0, 'leavers': 0, 'starters': 0, 'scores': []})
    with open('grind_and_crumb_data/staff_monthly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            staff_monthly[s]['headcount'] = int(r['headcount']) # last
            staff_monthly[s]['leavers'] += int(r['leavers'])
            staff_monthly[s]['starters'] += int(r['new_starters'])
            staff_monthly[s]['scores'].append(float(r['staff_survey_score_10']))

    print("\n=== STAFF TURNOVER & SURVEY BY STORE ===")
    for s in sorted(staff_monthly.keys()):
        d = staff_monthly[s]
        avg_score = sum(d['scores']) / len(d['scores'])
        # Turnover rate = total leavers / average headcount
        print(f"Store {s}: Headcount={d['headcount']}, Leavers={d['leavers']}, Starters={d['starters']}, Avg Survey={avg_score:.2f}/10")

    # 3. Staff Exit survey main reasons
    exit_reasons = Counter()
    with open('grind_and_crumb_data/staff_exit_survey.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            exit_reasons[r['main_reason']] += 1
    print("\n=== STAFF EXIT REASONS ===")
    for r, count in exit_reasons.most_common():
        print(f"{r}: {count}")

    # 4. Delivery basket analysis
    del_baskets = []
    del_orders_by_val = {'under_8': 0, '8_to_15': 0, '15_to_25': 0, 'over_25': 0}
    del_partner_basket = defaultdict(list)
    with open('grind_and_crumb_data/transactions.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['channel'] == 'Delivery':
                net = float(r['net_gbp'])
                del_baskets.append(net)
                p = r['delivery_partner']
                del_partner_basket[p].append(net)
                if net < 8.0:
                    del_orders_by_val['under_8'] += 1
                elif net < 15.0:
                    del_orders_by_val['8_to_15'] += 1
                elif net < 25.0:
                    del_orders_by_val['15_to_25'] += 1
                else:
                    del_orders_by_val['over_25'] += 1

    print(f"\n=== DELIVERY ORDERS (Sample size: {len(del_baskets)}) ===")
    print(f"Average Order Value: £{sum(del_baskets)/len(del_baskets):.2f}")
    for k, v in del_orders_by_val.items():
        print(f"Bracket {k}: {v} ({v/len(del_baskets)*100:.1f}%)")
    for p, vals in del_partner_basket.items():
        print(f"Partner {p}: Count={len(vals)}, AOV=£{sum(vals)/len(vals):.2f}")

    # 5. Customer reviews themes
    print("\n=== CUSTOMER REVIEWS RATING & THEMES ===")
    ratings = Counter()
    store_ratings = defaultdict(list)
    complaints = defaultdict(int)
    with open('grind_and_crumb_data/customer_reviews.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rate = int(r['rating'])
            ratings[rate] += 1
            txt = r['review_text'].lower()
            if 'oat' in txt: complaints['oat_milk'] += 1
            if 'app' in txt or 'stamp' in txt: complaints['app_bugs'] += 1
            if 'queue' in txt or 'wait' in txt: complaints['queue_wait'] += 1
            if 'cold' in txt or 'wrong' in txt: complaints['food_quality_order'] += 1
            if 'rude' in txt or 'staff' in txt: complaints['service_staff'] += 1
            if 'clean' in txt or 'dirty' in txt or 'table' in txt: complaints['cleanliness'] += 1

    print("Ratings distribution:", dict(ratings))
    print("Complaint keywords:", dict(complaints))

    # 6. Candidate sites evaluation
    print("\n=== CANDIDATE SITES ===")
    with open('grind_and_crumb_data/candidate_sites.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            print(f"{r['site_id']} | {r['site_name']:<26} | City: {r['city']:<10} | Fitout: £{int(r['est_fitout_gbp']):,} | Rent: £{int(r['quoted_rent_gbp_month']):,}/mo | Footfall: {int(r['daily_footfall_street']):,} | Vibrancy: {r['area_vibrancy_index_10']}/10")

deep_dive()
