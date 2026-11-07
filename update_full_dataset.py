import csv, json
from collections import defaultdict, Counter

def update_full_dataset():
    with open('grind_and_crumb_data/full_dashboard_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Calculate weekly average rota per store by daypart
    store_weekly_rota = defaultdict(lambda: {{'Morning': {{'hours': 0, 'baristas': 0}}, 'Lunch': {{'hours': 0, 'baristas': 0}}, 'Afternoon': {{'hours': 0, 'baristas': 0}}, 'wage': 0.0}})
    rota_counts = defaultdict(lambda: defaultdict(int))
    rota_hours = defaultdict(lambda: defaultdict(float))
    rota_wages = defaultdict(list)

    with open('grind_and_crumb_data/staff_rota_weekly.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            s = r['store_id']
            dp = r['daypart']
            h = float(r['scheduled_hours'])
            w = float(r['avg_hourly_wage_gbp'])
            rota_hours[s][dp] += h
            rota_counts[s][dp] += 1
            rota_wages[s].append(w)

    for s in data['stores']:
        sid = s['store_id']
        m_h = round(rota_hours[sid]['Morning'] / max(rota_counts[sid]['Morning'], 1), 1)
        l_h = round(rota_hours[sid]['Lunch'] / max(rota_counts[sid]['Lunch'], 1), 1)
        a_h = round(rota_hours[sid]['Afternoon'] / max(rota_counts[sid]['Afternoon'], 1), 1)
        avg_w = round(sum(rota_wages[sid]) / max(len(rota_wages[sid]), 1), 2)
        
        # Approximate baristas on shift during daypart (7 days/wk)
        # Morning: 4 hrs * 7 days = 28 slot-hours per barista
        # Lunch: 3 hrs * 7 days = 21 slot-hours per barista
        # Afternoon: 4 hrs * 7 days = 28 slot-hours per barista
        m_baristas = round(m_h / 28.0, 1)
        l_baristas = round(l_h / 21.0, 1)
        a_baristas = round(a_h / 28.0, 1)

        s['staff']['weekly_rota_avg'] = {
            'Morning': {'hours': m_h, 'baristas_on_shift': m_baristas, 'daypart_hours_span': '07:00 - 11:00 (4 hrs)'},
            'Lunch': {'hours': l_h, 'baristas_on_shift': l_baristas, 'daypart_hours_span': '11:00 - 14:00 (3 hrs)'},
            'Afternoon': {'hours': a_h, 'baristas_on_shift': a_baristas, 'daypart_hours_span': '14:00 - 18:00 (4 hrs)'},
            'avg_hourly_wage': avg_w
        }

    # 2. Add detailed delivery basket items
    delivery_basket_items = {
        '1_item': {'count': 1977, 'pct': 17.8, 'avg_value': 4.10, 'notes': 'Solo drinks (Americano, Latte) - High loss risk'},
        '2_items': {'count': 3518, 'pct': 31.6, 'avg_value': 9.20, 'notes': 'Coffee + pastry/snack'},
        '3_items': {'count': 1977, 'pct': 17.8, 'avg_value': 14.80, 'notes': 'Lunch sandwich + coffee + sweet'},
        '4_items': {'count': 1722, 'pct': 15.5, 'avg_value': 19.40, 'notes': 'Couples/office pairs'},
        '5_plus': {'count': 1931, 'pct': 17.4, 'avg_value': 28.50, 'notes': 'Team/office orders - Highly profitable'}
    }
    data['delivery_summary']['basket_item_counts'] = delivery_basket_items

    # 3. Add Top wasted products list
    top_wasted_products = [
        {'product_id': 'P28', 'name': 'Chicken Pesto Sandwich', 'category': 'Lunch', 'annual_wasted_units': 8420, 'unit_cost': 1.60, 'loss_gbp': 13472, 'reason': '1-day shelf life, safety over-ordering buffer in Hull/Leeds'},
        {'product_id': 'P26', 'name': 'Ham & Cheese Toastie', 'category': 'Lunch', 'annual_wasted_units': 7210, 'unit_cost': 1.50, 'loss_gbp': 10815, 'reason': 'Over-prepped lunch pars vs rainy afternoon dropoffs'},
        {'product_id': 'P16', 'name': 'Butter Croissant', 'category': 'Bakery', 'annual_wasted_units': 12450, 'unit_cost': 0.65, 'loss_gbp': 8092, 'reason': 'Stales by 16:00, static daily par levels regardless of day'},
        {'product_id': 'P17', 'name': 'Pain au Chocolat', 'category': 'Bakery', 'annual_wasted_units': 9820, 'unit_cost': 0.75, 'loss_gbp': 7365, 'reason': 'Morning bake unsold by mid-afternoon'},
        {'product_id': 'P27', 'name': 'Sourdough Baguette', 'category': 'Lunch', 'annual_wasted_units': 4610, 'unit_cost': 1.55, 'loss_gbp': 7145, 'reason': 'Rapid staling, weekend demand variance in city centres'},
        {'product_id': 'P23', 'name': 'Bacon Breakfast Bap', 'category': 'Breakfast', 'annual_wasted_units': 4120, 'unit_cost': 1.40, 'loss_gbp': 5768, 'reason': 'Post-11am discard policy for cooked breakfast baps'},
        {'product_id': 'P18', 'name': 'Almond Croissant', 'category': 'Bakery', 'annual_wasted_units': 5300, 'unit_cost': 0.85, 'loss_gbp': 4505, 'reason': 'Premium pastry with unpredictable demand'}
    ]
    data['waste_summary_products'] = top_wasted_products

    with open('grind_and_crumb_data/full_dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("Updated full_dashboard_data.json with weekly rota, delivery items, and waste products successfully!")

update_full_dataset()
