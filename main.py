from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import random

app = FastAPI(title="NEXUS Autonomous C-Suite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MIN_MARGIN_THRESHOLD = 0.30
TIMEZONE = pytz.timezone('America/Chicago')

# ---------------------------------------------------------
# VP OF PROCUREMENT: THE UNIVERSAL AGGREGATOR (PIPELINE)
# ---------------------------------------------------------
def hunt_global_suppliers(category: str):
    """
    In production, this connects to Zendrop/Spocket/CJ Dropshipping APIs.
    Right now, it simulates scraping 100+ items from the market.
    """
    print(f"VP OF PROCUREMENT: Scanning US 3PL Networks for {category}...")
    
    # Simulating a massive raw data pull from global APIs
    raw_pull = []
    for i in range(1, 50):
        cost = round(random.uniform(10.0, 150.0), 2)
        # Randomly generate prices to test the VP of Cash Flow's ruthlessness
        multiplier = random.uniform(1.1, 2.5) 
        price = round(cost * multiplier, 2)
        
        shipping_days = random.randint(2, 14)
        
        raw_pull.append({
            "sku": f"SUPPLIER-RAW-{i}",
            "name": f"Trending {category} Item {i}",
            "cost": cost,
            "price": price,
            "shipping_days": shipping_days,
            "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80"
        })
    return raw_pull

# ---------------------------------------------------------
# VP OF CASH FLOW: THE RUTHLESS AUDITOR
# ---------------------------------------------------------
def execute_margin_audit(raw_items):
    """
    Kills anything under 30% margin. 
    Kills anything over 7 days shipping.
    Keeps only the top 12 absolute best performers.
    """
    approved_vault = []
    killed_count = 0
    
    for item in raw_items:
        margin = (item['price'] - item['cost']) / item['price']
        
        # Enforce strict Executive Rules
        if margin >= MIN_MARGIN_THRESHOLD and item['shipping_days'] <= 7:
            approved_vault.append({
                "sku": f"ALBS-VERIFIED-{random.randint(1000,9999)}",
                "name": item['name'],
                "price": f"{item['price']:.2f}",
                "cost": item['cost'],
                "margin_pct": round(margin * 100, 1),
                "images": [item['img']],
                "shippingText": f"PRIORITY DISPATCH: {item['shipping_days']} DAYS",
                "rating": round(random.uniform(4.5, 5.0), 1),
                "specsAvailable": True,
                "videoAvailable": True if item['price'] > 50 else False
            })
        else:
            killed_count += 1
            
    # Sort by highest margin first, cap at Top 12 Kill Shots
    approved_vault.sort(key=lambda x: x['margin_pct'], reverse=True)
    top_12 = approved_vault[:12]
    
    return top_12, killed_count

# ---------------------------------------------------------
# DAILY OPERATIONS: THE SHIFT REPORT
# ---------------------------------------------------------
daily_ledgers = {}

@app.get("/api/matrix")
def get_matrix(category: str):
    # 1. The Hunt
    raw_market_data = hunt_global_suppliers(category)
    
    # 2. The Audit
    live_items, killed = execute_margin_audit(raw_market_data)
    
    # 3. Log for the CEO's Daily Shift Report
    daily_ledgers[category] = {
        "items_scanned": len(raw_market_data),
        "items_killed": killed,
        "live_inventory": len(live_items),
        "avg_margin": f"{sum(i['margin_pct'] for i in live_items) / len(live_items):.1f}%" if live_items else "0%"
    }
    
    if not live_items:
        return {"status": "sourcing", "items": []}
        
    return {"status": "live", "items": live_items}

@app.get("/api/ceo-report")
def generate_shift_report():
    """ 
    THE CEO DASHBOARD: 
    This is all you look at. It tells you exactly what the AI did today.
    """
    current_time = datetime.now(TIMEZONE)
    
    report = {
        "EXECUTIVE_SUMMARY": "ALBS DAILY SHIFT MATCHUP",
        "SHIFT_TIME": current_time.strftime("%Y-%m-%d %H:%M:%S CST"),
        "NEXT_RESET": "21:00:00 CST",
        "STOREFRONT_LEDGERS": daily_ledgers,
        "SYSTEM_STATUS": "AUTONOMOUS HUNTING ACTIVE. ALL MARGINS > 30%."
    }
    return report
