import json

with open('grind_and_crumb_data/full_dashboard_data.json', 'r', encoding='utf-8') as f:
    full_data_json = f.read()

# Verify json is valid
data = json.loads(full_data_json)
print(f"Loaded {len(data['stores'])} stores, {len(data['products'])} products, {len(data['candidate_sites'])} candidate sites.")
