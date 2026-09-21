from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz

app = FastAPI(title="ALBS Executive C-Suite")

# Opens the secure pipeline to your DigitalOcean frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI C-SUITE CONFIGURATION ---
MIN_MARGIN_THRESHOLD = 0.30  # 30% Minimum Profit Margin
TIMEZONE = pytz.timezone('America/Chicago') # Houston/Central Time

# --- VP OF PROCUREMENT: 30-40 SHOT MOCK DATABASE ---
RAW_INVENTORY = {
    "TRADING CARDS VAULT": [
        {"name": "The Executive Collector's Vault (Sealed)", "price": 495.00, "cost": 300.00, "img": "https://images.unsplash.com/photo-1628102491629-77858ab215b2?w=800&q=80", "ship": "PRIORITY DISPATCH: 72 HOURS", "testimonial": '"Flawless presentation. The centerpiece of my collection." - Verified Buyer'},
        {"name": "Graded Gem Mint Mystery Slab", "price": 150.00, "cost": 90.00, "img": "https://images.unsplash.com/photo-1640590326466-419b48f95c69?w=800&q=80", "ship": "SECURE ALLOCATION: 3-5 DAYS", "testimonial": None},
        {"name": "1999 Base Set Booster Pack (Heavy)", "price": 850.00, "cost": 500.00, "img": "https://images.unsplash.com/photo-1613771404721-1f92d799e49f?w=800&q=80", "ship": "ARMORED TRANSPORT: 3 DAYS", "testimonial": '"Weighed exactly as promised. Unbelievable pull." - Verified Buyer'},
        {"name": "Magnetic UV-Protected Display Cases (10-Pack)", "price": 45.00, "cost": 25.00, "img": "https://images.unsplash.com/photo-1584844007883-9b6260a927a3?w=800&q=80", "ship": "STANDARD PRIORITY: 5-7 DAYS", "testimonial": None},
        {"name": "Autographed Rookie Refractor (BGS 9.5)", "price": 1250.00, "cost": 750.00, "img": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800&q=80", "ship": "SECURE VAULT: 3 DAYS", "testimonial": '"Pristine condition. Fastest shipping I have ever seen on a high-end card." - Verified Buyer'}
    ],
    "TECH & MOBILE GEAR": [
        {"name": "Carbon Fiber EDC Smart Wallet", "price": 85.00, "cost": 45.00, "img": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80", "ship": "PRIORITY FULFILLMENT: 3-5 DAYS", "testimonial": None},
        {"name": "Titanium Wireless Charging Dock", "price": 120.00, "cost": 60.00, "img": "https://images.unsplash.com/photo-1586942512683-162128ce3722?w=800&q=80", "ship": "EXPRESS DISPATCH: 3 DAYS", "testimonial": '"Looks incredible on my executive desk. Heavy, premium feel." - Verified Buyer'},
        {"name": "Noise-Cancelling Tactical Earbuds", "price": 199.00, "cost": 110.00, "img": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80", "ship": "PRIORITY ALLOCATION: 5 DAYS", "testimonial": None},
        {"name": "Air-Gapped External Encrypted Drive (2TB)", "price": 350.00, "cost": 190.00, "img": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=800&q=80", "ship": "SECURE LOGISTICS: 3-7 DAYS", "testimonial": '"Absolute peace of mind. The encryption protocols are military grade." - Verified Buyer'},
        {"name": "Executive Privacy Screen & Armor Glass", "price": 55.00, "cost": 15.00, "img": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=800&q=80", "ship": "STANDARD PRIORITY: 3-5 DAYS", "testimonial": None}
    ],
    "TRAVEL EDC ESSENTIALS": [
        {"name": "Ballistic Nylon Weekender Duffel", "price": 225.00, "cost": 110.00, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80", "ship": "PRIORITY FULFILLMENT: 3-5 DAYS", "testimonial": '"The last travel bag I will ever buy. Fits perfectly in overhead." - Verified Buyer'},
        {"name": "TSA-Approved Biometric Padlock", "price": 95.00, "cost": 40.00, "img": "https://images.unsplash.com/photo-1558004240-410a05a1e2f7?w=800&q=80", "ship": "EXPRESS DISPATCH: 3 DAYS", "testimonial": None},
        {"name": "Global 100W Travel Adapter & Hub", "price": 75.00, "cost": 30.00, "img": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&q=80", "ship": "SECURE ALLOCATION: 5-7 DAYS", "testimonial": None},
        {"name": "Grade-5 Titanium Tactical Pen", "price": 115.00, "cost": 50.00, "img": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=800&q=80", "ship": "PRIORITY DISPATCH: 3-5 DAYS", "testimonial": '"Writes smoothly and feels indestructible." - Verified Buyer'},
        {"name": "RFID-Blocking Passport Vault", "price": 65.00, "cost": 25.00, "img": "https://images.unsplash.com/photo-1553835973-dec43bfddbeb?w=800&q=80", "ship": "STANDARD PRIORITY: 3-7 DAYS", "testimonial": None}
    ],
    # COMING SOON ROOMS
    "PET LIFESTYLE BAR": [],
    "KITCHEN SMART GADGETS": [],
    "CURATED MYSTERY BOXES": []
}

def audit_cash_flow(category_items):
    """ VP OF CASH FLOW AUDITS: Enforces 30% margins """
    approved_inventory = []
    for item in category_items:
        margin = (item['price'] - item['cost']) / item['price']
        if margin >= MIN_MARGIN_THRESHOLD:
            approved_inventory.append({
                "sku": f"ALBS-{str(hash(item['name']))[-6:]}",
                "name": item['name'],
                "price": f"{item['price']:.2f}",
                "images": [item['img']],
                "testimonial": item['testimonial'],
                "rating": 5.0 if item['testimonial'] else 4.8,
                "specsAvailable": True,
                "videoAvailable": True if item['price'] > 100 else False,
                "shippingText": item['ship']
            })
    return approved_inventory

@app.get("/api/matrix")
def get_matrix(category: str):
    # VP of Operations: Daily Reset Check (9:00 PM CST)
    current_time = datetime.now(TIMEZONE)
    if current_time.hour == 21 and current_time.minute == 0:
        print("EXECUTING DAILY 9:00 PM CST SHIFT RESET...")
        
    if category in RAW_INVENTORY:
        raw_items = RAW_INVENTORY[category]
        if not raw_items:
            # Trigger the "Coming Soon / Sourcing" UI
            return {"status": "sourcing", "items": []}
            
        # Pass to Cash Flow VP for 30% margin audit
        live_items = audit_cash_flow(raw_items)
        return {"status": "live", "items": live_items}
        
    raise HTTPException(status_code=404, detail="Category not found")
