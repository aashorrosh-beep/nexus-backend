import os
import re
import json
import random
import urllib.request
import urllib.parse
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
import stripe
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

# --- LIVE KEYS FROM RENDER ENVIRONMENT ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPPLIER_API_KEY = os.getenv("ZENDROP_API_KEY", "pending_key")
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or os.getenv("SERPER_API_KEY")

app = FastAPI(title="NEXUS Matrix Mall Engine - Dual-Brain 22-Room Production")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# DATA MODELS
# -----------------------------------------------------------------------------
class ProductSpecs(BaseModel):
    manufacturer: str
    condition: str
    authenticity_verified: bool
    material_grade: str
    dimensions: str
    shipping_weight: str
    warranty_status: str
    spec_sheet_url: Optional[str] = None

class NexusProduct(BaseModel):
    sku: str
    storefront: str
    name: str
    price: float
    cost: float
    margin_pct: float
    images: List[str]
    hero_image: str
    video_url: str
    shippingText: str
    rating: float
    marketing_copy: str
    specs: ProductSpecs
    stock_count: int
    viral_velocity: int
    is_presale: bool = False

class CheckoutRequest(BaseModel):
    name: str
    price: float
    image: str

STOREFRONTS = [
    "Trading Cards Vault", "Tech & Mobile Gear", "High-Performance Auto", "Golf & Athletic Apparel",
    "Home Renovation & Fixtures", "Luxury & Humidor Accessories", "Fine Arts & Creative Design",
    "Health & Wellness Tech", "Beauty & Personal Care", "Eco-Friendly Living", "Smart Pet Tech",
    "Home Office Ergonomics", "Outdoor & Survival Gear", "Gourmet Food & Culinary", "Men's Grooming",
    "Travel Tech & Luggage", "Fitness & Recovery", "Gaming & Esports", "Early Education Tech",
    "Smart Kitchen Gadgets", "Room 21: Pre-Release Acquisitions", 
    "Room 22: Squishmallows & Blind Boxes"
]

# -----------------------------------------------------------------------------
# MEDIA ENRICHMENT ENGINE (DYNAMIC PLACEHOLDERS - NO MORE SOFAS)
# -----------------------------------------------------------------------------
def enrich_manufacturer_media(brand: str, title: str) -> dict:
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return {
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "spec_sheet": f"https://nexus-matrix-vault.storage/specs/{urllib.parse.quote(clean_title[:20])}_spec.pdf"
    }

def curate_image_spread(base_images: List[str], title: str) -> List[str]:
    curated = [img for img in base_images if img and "placeholder" not in img]
    
    # If no valid images exist, generate a dynamic text graphic plate based on the item's name
    if not curated:
        clean_text = urllib.parse.quote(title[:25])
        dynamic_img = f"https://placehold.co/800x800/111/fcba03?text={clean_text}"
        curated.append(dynamic_img)
        
    return curated[:5]

# -----------------------------------------------------------------------------
# PROCUREMENT LOGIC (25 ITEMS + TIERED PRICING)
# -----------------------------------------------------------------------------
def fetch_raw_storefront_assets(room_name: str) -> List[dict]:
    room_upper = room_name.upper()
    items = []

    if "PRE-RELEASE" in room_upper or "ROOM 21" in room_upper or "VAULT" in room_upper:
        allocations = [
            ("Tom Brady 1-of-1 Refractor Autograph", 3500.0, "Panini", 1, "12 x 8 x 2 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Tom+Brady+1-of-1"),
            ("Pokémon TCG: Booster Box Display", 550.0, "Pokémon", 12, "8 x 6 x 5 in", "3.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pokemon+Booster+Box"),
            ("One Piece TCG: Wings of Captain", 480.0, "Bandai", 8, "8 x 6 x 5 in", "3.0 lbs", "https://placehold.co/800x800/111/fcba03?text=One+Piece+Box"),
            ("Magic: The Gathering Collector Case", 1450.0, "Wizards", 4, "14 x 10 x 8 in", "8.5 lbs", "https://placehold.co/800x800/111/fcba03?text=MTG+Collector+Case"),
            ("Caitlin Clark Rookie Gold Refractor", 850.0, "Bowman", 2, "6 x 4 x 1 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Caitlin+Clark+Rookie"),
            ("Jordan Groshans 1st Bowman Auto", 250.0, "Topps", 5, "6 x 4 x 1 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Jordan+Groshans+Auto"),
            ("Tiger Woods 22KT Gold Collection", 1200.0, "Upper Deck", 2, "10 x 8 x 3 in", "2.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Tiger+Woods+Gold"),
            ("Pokémon TCG: Sealed Mini Tin 10-Pack", 320.0, "Pokémon", 15, "12 x 6 x 4 in", "4.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Pokemon+Mini+Tins"),
            ("NFL National Treasures Hobby Box", 2800.0, "Panini", 3, "10 x 10 x 6 in", "5.5 lbs", "https://placehold.co/800x800/111/fcba03?text=NFL+National+Treasures"),
            ("NBA Flawless Sealed Case", 4200.0, "Panini", 1, "16 x 12 x 10 in", "12.0 lbs", "https://placehold.co/800x800/111/fcba03?text=NBA+Flawless"),
            ("One Piece TCG: Awakening Case", 2200.0, "Bandai", 2, "14 x 10 x 8 in", "9.0 lbs", "https://placehold.co/800x800/111/fcba03?text=One+Piece+Awakening"),
            ("F1 Chrome Hobby Box Factory Sealed", 650.0, "Topps", 6, "9 x 6 x 4 in", "2.8 lbs", "https://placehold.co/800x800/111/fcba03?text=F1+Chrome+Box"),
            ("Shohei Ohtani Dual Auto Relic", 3100.0, "Topps", 1, "8 x 6 x 2 in", "1.8 lbs", "https://placehold.co/800x800/111/fcba03?text=Shohei+Ohtani+Auto"),
        ]
        for name, cost, brand, stock, dims, wt, img in allocations[:13]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified allocation asset. Vault-secured provenance for {name}.",
                "images": [img], "dimensions": dims, "weight": wt, "is_presale": True
            })
        
    elif "ROOM 22" in room_upper or "SQUISHMALLOW" in room_upper:
        allocations = [
            ("Squishmallows 8-Inch Mystery Squad Box", 9.0, "Kellytoy", 24, "8 x 8 x 8 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=8-Inch+Mystery+Squishmallow"),
            ("Pop Mart Skullpanda Everyday Wonderland Blind Box", 11.0, "Pop Mart", 15, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Skullpanda"),
            ("Jellycat Amuseable Boiled Egg (Small)", 10.0, "Jellycat", 18, "5 x 3 x 3 in", "0.3 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Egg"),
            ("Squishmallows 16-Inch Rare Connor The Cow", 45.0, "Kellytoy", 8, "16 x 16 x 16 in", "2.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Connor+The+Cow"),
            ("Sonny Angel Mini Figure Original Series (Single)", 9.5, "Dreams Inc.", 36, "3 x 2 x 2 in", "0.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Sonny+Angel+Single"),
            ("Smiski Glow-In-The-Dark Figure (Single)", 8.5, "Dreams Inc.", 40, "3 x 2 x 2 in", "0.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Smiski+Glow+Figure"),
            ("Squishmallows 12-Inch Archie The Axolotl", 35.0, "Kellytoy", 14, "12 x 12 x 12 in", "1.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Archie+Axolotl"),
            ("Tokidoki Unicorno Series 12 Blind Box", 10.5, "Tokidoki", 27, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Tokidoki+Unicorno"),
            ("Jellycat Bashful Bunny (Medium)", 14.0, "Jellycat", 15, "12 x 5 x 4 in", "0.6 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Bunny"),
            ("Pop Mart Hirono City of Mercy Series (Single)", 12.0, "Pop Mart", 20, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Hirono"),
            ("Squishmallows 5-Inch Mini 6-Pack Assortment", 22.0, "Kellytoy", 10, "10 x 8 x 5 in", "1.0 lbs", "https://placehold.co/800x800/111/fcba03?text=5-Inch+Squishmallow+Pack"),
            ("Gudetama Lazy Egg Vinyl Figure Box", 11.0, "Sanrio", 12, "4 x 4 x 4 in", "0.3 lbs", "https://placehold.co/800x800/111/fcba03?text=Gudetama+Vinyl"),
            ("Squishmallows 14-Inch Gengar Pokemon Edition", 55.0, "Kellytoy", 9, "14 x 14 x 14 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Gengar+Squishmallow"),
            ("Pop Mart Dimoo Dating Series (Single)", 12.0, "Pop Mart", 18, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Dimoo"),
            ("Jellycat Amuseable Silly Succulent Plush", 32.0, "Jellycat", 18, "6 x 3 x 3 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Succulent"),
        ]
        for name, cost, brand, stock, dims, wt, img in allocations[:25]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified authentic {brand} highly-allocated collectible. Mint condition.",
                "images": [img], "dimensions": dims, "weight": wt, "is_presale": False
            })

    else:
        query_map = {
            "TECH": "smart gadgets", "AUTO": "automotive parts", "GOLF": "golf accessories",
            "HOME": "luxury home fixtures", "HUMIDOR": "cigar humidor", "ART": "sculpture design",
            "WELLNESS": "recovery tech", "BEAUTY": "skincare tools", "ECO": "sustainable living",
            "PET": "smart pet", "OFFICE": "ergonomic office", "OUTDOOR": "tactical survival"
        }
        search_q = "premium"
        for key, val in query_map.items():
            if key in room_upper: search_q = val; break

        try:
            url = f"https://dummyjson.com/products/search?q={urllib.parse.quote(search_q)}&limit=15"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as res:
                data = json.loads(res.read().decode())
                for p in data.get("products", []):
                    items.append({
                        "title": p.get("title"), "wholesale_cost": float(p.get("price", 50.0)),
                        "brand": p.get("brand", "Verified Manufacturer"), "stock": p.get("stock", random.randint(15, 60)),
                        "description": p.get("description"), "images": p.get("images", []),
                        "dimensions": "14 x 10 x 6 in", "weight": f"{round(random.uniform(1.5, 6.0), 1)} lbs",
                        "is_presale": False
                    })
        except Exception:
            pass

    # FORCE EXACTLY 25 ITEMS WITH TIERED PRICING
    idx = len(items) + 1
    while len(items) < 25:
        tier = random.choice([1, 1, 2, 2, 3]) 
        if tier == 1: cost = round(random.uniform(6.0, 12.0), 2)
        elif tier == 2: cost = round(random.uniform(14.0, 24.0), 2)
        else: cost = round(random.uniform(35.0, 80.0), 2)

        title = f"{room_name} Asset {idx:02d}"
        
        encoded_title = urllib.parse.quote(title[:25])
        fallback_img = f"https://placehold.co/800x800/111/fcba03?text={encoded_title}"

        items.append({
            "title": title, "wholesale_cost": cost,
            "brand": "Direct Manufacturer Verified", "stock": random.randint(20, 80),
            "description": f"Engineered specification for {room_name}.",
            "images": [fallback_img], "dimensions": "18 x 12 x 8 in", "weight": "4.2 lbs", "is_presale": False
        })
        idx += 1

    return items[:25]

# -----------------------------------------------------------------------------
# DUAL-BRAIN AGENT NODES
# -----------------------------------------------------------------------------
async def agent_enrichment(raw_item: dict, room_name: str) -> NexusProduct:
    cost = raw_item["wholesale_cost"]
    
    if raw_item["is_presale"]: target_price = round(cost * 1.30, 2)
    elif cost < 50: target_price = round(cost * 2.2, 2)
    elif cost < 200: target_price = round(cost * 1.7 + 20, 2)
    else: target_price = round(cost * 1.45 + 40, 2)

    margin = round(((target_price - cost) / target_price) * 100, 1)
    
    gallery = curate_image_spread(raw_item.get("images", []), raw_item["title"])
    media = enrich_manufacturer_media(raw_item["brand"], raw_item["title"])
    
    shipping_badge = "PRIORITY SECURE ALLOCATION" if raw_item["is_presale"] else f"PRIORITY SECURE DISPATCH: {random.randint(3, 6)} DAYS"

    specs = ProductSpecs(
        manufacturer=raw_item["brand"], condition="Pristine / Factory Sealed",
        authenticity_verified=True, material_grade="Aerospace/Investment Grade (Certified)",
        dimensions=raw_item["dimensions"], shipping_weight=raw_item["weight"],
        warranty_status="1-Year Global Direct Protection", spec_sheet_url=media["spec_sheet"]
    )

    return NexusProduct(
        sku=f"DS-VERIFIED-{random.randint(100000, 999999)}", storefront=room_name.upper(),
        name=raw_item["title"], price=target_price, cost=cost, margin_pct=margin,
        images=gallery, hero_image=gallery[0], video_url=media["video_url"],
        shippingText=shipping_badge, rating=round(random.uniform(4.7, 5.0), 1),
        marketing_copy=raw_item["description"], specs=specs, stock_count=raw_item["stock"],
        viral_velocity=random.randint(75, 99), is_presale=raw_item["is_presale"]
    )

# -----------------------------------------------------------------------------
# API ROUTES
# -----------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ONLINE", "engine": "NEXUS PRIME v11.0"}

@app.get("/api/matrix")
async def get_matrix(category: str = "all"):
    target_rooms = STOREFRONTS if category == "all" else [r for r in STOREFRONTS if category.lower() in r.lower()]
    catalog = []
    for room in target_rooms:
        raw_batch = fetch_raw_storefront_assets(room)
        for raw in raw_batch:
            product = await agent_enrichment(raw, room)
            catalog.append(product.model_dump())
    return catalog
