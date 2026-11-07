import csv

def evaluate_sites():
    print("=== CANDIDATE SITES INVESTMENT APPRAISAL ===")
    sites = []
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

            # Benchmark model against existing 12 stores:
            # Conversion rate ~ 1.5% - 2.5% of street footfall
            # Or estimated annual sales based on format and footfall
            est_annual_sales = min(max(footfall * 25.0 * (vibrancy / 7.0), 450000), 950000)
            
            # Penalize for cannibalization:
            cannibalization_risk = 'None'
            if r['city'] == 'Leeds':
                if 'Wellington' in r['site_name']:
                    cannibalization_risk = 'VERY HIGH (Leeds already has Briggate S03 & Trinity S12 within 0.5 miles!)'
                    est_annual_sales *= 0.75 # cannibalized
                elif 'Headingley' in r['site_name']:
                    cannibalization_risk = 'Low (Suburban student area 2.5 miles from city centre)'
            elif r['city'] == 'Sheffield':
                if 'Kelham' in r['site_name']:
                    cannibalization_risk = 'Low (Separate hipster regeneration district 1 mile from Division St)'
            elif r['city'] == 'Manchester':
                if 'Oxford' in r['site_name']:
                    cannibalization_risk = 'Medium (High student density, distinct from NQ and Piccadilly)'

            # Est costs: COGS 27.4%, Labour ~ 28%, Rent + rates (rates ~ 22% of rent), Opex ~ £40k
            cogs = est_annual_sales * 0.274
            labour = est_annual_sales * 0.28
            rates = rent_yr * 0.22
            opex = 45000
            deliv_costs = (est_annual_sales * 0.15) * 0.30 # 15% delivery with 30% fee
            est_costs = cogs + labour + rent_yr + rates + opex + deliv_costs
            est_ebitda = est_annual_sales - est_costs
            est_margin = (est_ebitda / est_annual_sales) * 100
            payback_years = fitout / est_ebitda if est_ebitda > 0 else 99.0

            sites.append({
                'id': r['site_id'],
                'name': r['site_name'],
                'city': r['city'],
                'fitout': fitout,
                'rent_yr': rent_yr,
                'sales': est_annual_sales,
                'ebitda': est_ebitda,
                'margin': est_margin,
                'payback': payback_years,
                'cannibalization': cannibalization_risk
            })

    sites.sort(key=lambda x: x['payback'])
    for s in sites:
        print(f"{s['id']} | {s['name']:<24} | Fitout: £{s['fitout']:>7,.0f} | Est Sales: £{s['sales']:>8,.0f} | Est EBITDA: £{s['ebitda']:>7,.0f} ({s['margin']:>4.1f}%) | Payback: {s['payback']:>4.1f} yrs | Risk: {s['cannibalization']}")

evaluate_sites()
