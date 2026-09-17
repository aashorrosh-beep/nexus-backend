import time
import random

# The 14 Expanded Vaults
CATEGORIES = [
    "electronics", "athletics", "apparel", "wellness",
    "sports_collectibles", "automotive_performance", "premium_cigars", "golf_equipment",
    "home_architecture", "fine_arts", "tactical_supply", "maritime_tech",
    "culinary_pro", "network_security"
]

# Raw Data Lake (Unsorted, Unfiltered)
RAW_DATALAKE = [
    {"cat": "sports_collectibles", "sku": "sc_001", "name": "Tom Brady 1-of-1 Autograph", "price": 3500.00, "searches": 942, "conversion_rate": 0.12},
    {"cat": "sports_collectibles", "sku": "sc_002", "name": "Caitlin Clark Rookie Refractor", "price": 450.00, "searches": 1205, "conversion_rate": 0.18},
    {"cat": "golf_equipment", "sku": "ge_001", "name": "Topographic Green Relief Map", "price": 110.00, "searches": 340, "conversion_rate": 0.22},
    {"cat": "automotive_performance", "sku": "ap_001", "name": "Demon 170 ECU Tuner", "price": 899.99, "searches": 560, "conversion_rate": 0.08},
    {"cat": "network_security", "sku": "ns_001", "name": "NFC Hardware Key Vault", "price": 75.00, "searches": 920, "conversion_rate": 0.25},
    {"cat": "premium_cigars", "sku": "pc_001", "name": "Authentic Habano Maduro Series", "price": 240.00, "searches": 410, "conversion_rate": 0.15},
    {"cat": "athletics", "sku": "ath_001", "name": "Athletic 360 Performance Middleware", "price": 150.00, "searches": 880, "conversion_rate": 0.21},
    {"cat": "wellness", "sku": "well_001", "name": "Smart Life Protocol Integration", "price": 299.99, "searches": 670, "conversion_rate": 0.19},
    {"cat": "home_architecture", "sku": "ha_001", "name": "CityPost Cable Railing Kit", "price": 450.00, "searches": 210, "conversion_rate": 0.30},
]

# Generate additional background noise data for the engine to sort through
for cat in CATEGORIES:
    for i in range(15):
        RAW_DATALAKE.append({
            "cat": cat,
            "sku": f"{cat[:3]}_test_{i}",
            "name": f"Standard {cat.replace('_', ' ').title()} Item {i}",
            "price": round(random.uniform(20.0, 500.0), 2),
            "searches": random.randint(50, 1000),
            "conversion_rate": round(random.uniform(0.01, 0.25), 3)
        })

def nexus_matchmaker_engine(datalake):
    print("\n[>>>] IGNITING NEXUS MATCHMAKER ENGINE...")
    time.sleep(1)
    print("[>>>] SCANNING 14 CATEGORY VAULTS...")
    time.sleep(1)
    
    trending_inventory = {cat: [] for cat in CATEGORIES}
    
    for item in datalake:
        # THE FORMULA: Trending Score = (Search Volume * Conversion Rate) / 10
        trending_score = (item["searches"] * item["conversion_rate"]) / 10
        item["trending_score"] = round(trending_score, 2)
        
        # Tag generation based on score threshold
        if trending_score > 15.0:
            item["tag"] = "VIRAL ALERT"
        elif trending_score > 10.0:
            item["tag"] = "TRENDING"
        else:
            item["tag"] = "SELLING FAST"
            
        trending_inventory[item["cat"]].append(item)

    print("[>>>] EXECUTING ALGORITHMIC SORTING...\n")
    time.sleep(1)
    
    # Sort each category by highest trending score and cap at top 5
    for cat in CATEGORIES:
        trending_inventory[cat] = sorted(trending_inventory[cat], key=lambda x: x["trending_score"], reverse=True)[:5]
        
        print(f"--- TOP TRENDING: {cat.replace('_', ' ').upper()} ---")
        for rank, product in enumerate(trending_inventory[cat], 1):
            print(f" #{rank} | {product['name']} | ${product['price']} | Score: {product['trending_score']} | [{product['tag']}]")
        print("-" * 50)

    return trending_inventory

if __name__ == "__main__":
    final_roster = nexus_matchmaker_engine(RAW_DATALAKE)
    print("\n[$$$] ALGORITHM COMPLETE. 14 VAULTS OPTIMIZED FOR SHOWROOM FLOOR.")
