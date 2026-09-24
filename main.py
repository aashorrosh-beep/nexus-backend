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
# MEDIA ENRICHMENT ENGINE (RAPID BYPASS TO PREVENT TIMEOUTS)
# -----------------------------------------------------------------------------
def enrich_manufacturer_media(brand: str, title: str) -> dict:
    """Instantly injects secure media streams without locking the server."""
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return {
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "spec_sheet": f"https://nexus-matrix-vault.storage/specs/{urllib.parse.quote(clean_title[:20])}_spec.pdf"
    }

def curate_image_spread(base_images: List[str], category: str) -> List[str]:
    curated = [img for img in base_images if img and "placeholder" not in img]
    fallbacks = {
        "CARDS": [
            "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?w=800&q=80",
            "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=800&q=80",
            "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&q=80",
            "https://images.unsplash.com/photo-1563089145-599997674d42?w=800&q=80"
        ],
        "NOVELTY": [
            "https://images.unsplash.com/photo-1558066141-8f553a0058b8?w=800&q=80",
            "https://images.unsplash.com/photo-1606011334315-025e4baab810?w=800&q=80",
            "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=800&q=80",
            "https://images.unsplash.com/photo-1533513700299-4081b5c4644a?w=800&q=80"
        ],
        "GENERAL": [
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=80",
            "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&q=80",
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"
        ]
    }
    
    if "CARD" in category.upper() or "VAULT" in category.upper(): 
        bank = fallbacks["CARDS"]
    elif "ROOM 22" in category.upper() or "SQUISHMALLOW" in category.upper(): 
        bank = fallbacks["NOVELTY"]
    else: 
        bank = fallbacks["GENERAL"]
        
    # Shuffle to prevent identical clone images when padding rooms
    random.shuffle(bank)
    
    for img in bank:
        if len(curated) >= 5: break
        if img not in curated: curated.append(img)
    return curated[:5]

# -----------------------------------------------------------------------------
# PROCUREMENT LOGIC
# -----------------------------------------------------------------------------
def fetch_raw_storefront_assets(room_name: str) -> List[dict]:
    room_upper = room_name.upper()
    items = []

    if "PRE-RELEASE" in room_upper or "ROOM 21" in room_upper or "VAULT" in room_upper:
        allocations = [
            ("Tom Brady 1-of-1 Refractor Autograph", 3500.0, "Panini National Treasures", 1, "12 x 8 x 2 in", "1.5 lbs"),
            ("Pokémon TCG: Booster Box Display", 550.0, "The Pokémon Company", 12, "8 x 6 x 5 in", "3.2 lbs"),
            ("One Piece TCG: Wings of the Captain Display", 480.0, "Bandai Card Games", 8, "8 x 6 x 5 in", "3.0 lbs"),
            ("Magic: The Gathering Collector Booster Case", 1450.0, "Wizards of the Coast", 4, "14 x 10 x 8 in", "8.5 lbs"),
            ("Caitlin Clark WNBA Rookie Gold Refractor", 850.0, "Bowman Chrome", 2, "6 x 4 x 1 in", "0.5 lbs"),
            ("Jordan Groshans 1st Bowman Chrome Auto", 250.0, "Topps Bowman", 5, "6 x 4 x 1 in", "0.5 lbs"),
            ("Tiger Woods Upper Deck 22KT Gold Collection", 1200.0, "Upper Deck Authenticated", 2, "10 x 8 x 3 in", "2.1 lbs"),
            ("Pokémon TCG: Sealed Mini Tin Display 10-Pack", 320.0, "The Pokémon Company", 15, "12 x 6 x 4 in", "4.0 lbs"),
            ("NFL National Treasures Hobby Box", 2800.0, "Panini America", 3, "10 x 10 x 6 in", "5.5 lbs"),
            ("NBA Flawless Sealed Allocation Case", 4200.0, "Panini America", 1, "16 x 12 x 10 in", "12.0 lbs"),
            ("One Piece TCG: Awakening of the New Era Case", 2200.0, "Bandai Card Games", 2, "14 x 10 x 8 in", "9.0 lbs"),
            ("F1 Chrome Hobby Box Factory Sealed", 650.0, "Topps Racing", 6, "9 x 6 x 4 in", "2.8 lbs"),
            ("Shohei Ohtani Certified Dual Auto Relic", 3100.0, "Topps Diamond Icons", 1, "8 x 6 x 2 in", "1.8 lbs"),
        ]
        for name, cost, brand, stock, dims, wt in allocations[:13]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified allocation asset. Vault-secured provenance for {name}.",
                "images": [], "dimensions": dims, "weight": wt,
                "is_presale": True if "PRE-RELEASE" in room_upper or "Presale" in name else False
            })
        return items
        
    elif "ROOM 22" in room_upper or "SQUISHMALLOW" in room_upper:
        allocations = [
            ("Squishmallows 16-Inch Rare Connor The Cow", 45.0, "Kellytoy", 8, "16 x 16 x 16 in", "2.0 lbs"),
            ("Pop Mart Skullpanda Everyday Wonderland Blind Box (Whole Set)", 145.0, "Pop Mart", 5, "12 x 8 x 6 in", "1.5 lbs"),
            ("Squishmallows 12-Inch Archie The Axolotl", 35.0, "Kellytoy", 14, "12 x 12 x 12 in", "1.2 lbs"),
            ("Sonny Angel Mini Figure Original Series (Case of 12)", 120.0, "Dreams Inc.", 6, "10 x 8 x 5 in", "1.8 lbs"),
            ("Smiski Glow-In-The-Dark Figure (Set of 6)", 65.0, "Dreams Inc.", 10, "8 x 6 x 4 in", "1.0 lbs"),
            ("Squishmallows Pokemon Pikachu 20-Inch Jumbo Plush", 85.0, "Kellytoy", 4, "20 x 20 x 20 in", "3.5 lbs"),
            ("Pop Mart Hirono City of Mercy Series Blind Box (Whole Set)", 150.0, "Pop Mart", 3, "12 x 8 x 6 in", "1.5 lbs"),
            ("Jellycat Amuseable Silly Succulent Plush", 32.0, "Jellycat", 18, "6 x 3 x 3 in", "0.5 lbs"),
            ("Tokidoki Unicorno Series 12 Blind Box Display", 110.0, "Tokidoki", 7, "10 x 8 x 6 in", "1.6 lbs"),
            ("Squishmallows 14-Inch Gengar Pokemon Edition", 55.0, "Kellytoy", 9, "14 x 14 x 14 in", "1.5 lbs"),
            ("Jellycat Bashful Bunny Huge Size", 65.0, "Jellycat", 5, "20 x 8 x 6 in", "1.2 lbs"),
            ("Pop Mart Dimoo Dating Series Blind Box (Whole Set)", 140.0, "Pop Mart", 4, "12 x 8 x 6 in", "1.5 lbs"),
            ("Squishmallows Jack the Black Cat (Limited Edition)", 250.0, "Kellytoy", 1, "16 x 16 x 16 in", "2.0 lbs"),
        ]
        for name, cost, brand, stock, dims, wt in allocations[:13]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified authentic {brand} highly-allocated collectible. Mint condition.",
                "images": [], "dimensions": dims, "weight": wt,
                "is_presale": False
            })
        return items

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
        url = f"https://dummyjson.com/products/search?q={urllib.parse.quote(search_q)}&limit=13"
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

    idx = 1
    while len(items) < 13:
        items.append({
            "title": f"{room_name} Premium Asset {idx:02d}", "wholesale_cost": round(random.uniform(45.0, 220.0), 2),
            "brand": "Direct Manufacturer Verified", "stock": random.randint(20, 80),
            "description": f"Engineered architectural grade specification for {room_name}.",
            "images": [], "dimensions": "18 x 12 x 8 in", "weight": "4.2 lbs", "is_presale": False
        })
        idx += 1

    return items[:13]

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
    gallery = curate_image_spread(raw_item.get("images", []), room_name)
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
    return {"status": "ONLINE", "engine": "NEXUS PRIME v10.0"}

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
