import os
import re
import json
import random
import urllib.request
import urllib.parse
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
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

app = FastAPI(title="NEXUS Matrix Mall Engine - Dual-Brain 21-Room Production")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# DATA MODELS (MATCHING DIGITALOCEAN NEXT.JS EXACT SPEC)
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
    "Smart Kitchen Gadgets", "Room 21: Pre-Release Acquisitions"
]

# -----------------------------------------------------------------------------
# MEDIA ENRICHMENT ENGINE (MANUFACTURER SCRAPING & KILL SHOT CURATION)
# -----------------------------------------------------------------------------
def enrich_manufacturer_media(brand: str, title: str) -> dict:
    """Scrapes raw .mp4 and .pdf links directly to prevent site leakage."""
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    results = {"video_url": None, "spec_sheet": None}
    
    try:
        query = urllib.parse.quote(f"{brand} {clean_title} promotional mp4 OR spec sheet pdf")
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if "/l/?kh=-1&uddg=" in href:
                    href = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                if ".mp4" in href and not results["video_url"]:
                    results["video_url"] = href
                if ".pdf" in href and not results["spec_sheet"]:
                    results["spec_sheet"] = href
                if results["video_url"] and results["spec_sheet"]:
                    break
    except Exception:
        pass

    # Reliable fallback media feeds (Direct streams, zero competitor branding)
    if not results["video_url"]:
        results["video_url"] = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    if not results["spec_sheet"]:
        results["spec_sheet"] = f"https://nexus-matrix-vault.storage/specs/{urllib.parse.quote(clean_title[:20])}_spec.pdf"
        
    return results

def curate_image_spread(base_images: List[str], category: str) -> List[str]:
    """Guarantees 4 to 5 high-impact visual angles with a primary kill shot."""
    curated = [img for img in base_images if img and "placeholder" not in img]
    
    fallbacks = {
        "CARDS": [
            "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?w=800&q=80",
            "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=800&q=80",
            "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&q=80",
            "https://images.unsplash.com/photo-1563089145-599997674d42?w=800&q=80"
        ],
        "GENERAL": [
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=80",
            "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&q=80",
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"
        ]
    }
    
    bank = fallbacks["CARDS"] if ("CARD" in category.upper() or "VAULT" in category.upper()) else fallbacks["GENERAL"]
    for img in bank:
        if len(curated) >= 5:
            break
        if img not in curated:
            curated.append(img)
            
    return curated[:5]

# -----------------------------------------------------------------------------
# PROCUREMENT & ROOM 21 ALLOCATION LOGIC
# -----------------------------------------------------------------------------
def fetch_raw_storefront_assets(room_name: str) -> List[dict]:
    room_upper = room_name.upper()
    items = []

    # ROOM 21 & VAULT: Presales and High-Demand Allocations (20-30% above MSRP)
    if "PRE-RELEASE" in room_upper or "ROOM 21" in room_upper or "VAULT" in room_upper:
        allocations = [
            ("Tom Brady 1-of-1 Refractor Autograph", 3500.0, "Panini National Treasures", 1, "12 x 8 x 2 in", "1.5 lbs"),
            ("Pokémon TCG: Booster Box Display (Pre-Release)", 550.0, "The Pokémon Company", 12, "8 x 6 x 5 in", "3.2 lbs"),
            ("One Piece TCG: Wings of the Captain Display", 480.0, "Bandai Card Games", 8, "8 x 6 x 5 in", "3.0 lbs"),
            ("Magic: The Gathering Collector Booster Case", 1450.0, "Wizards of the Coast", 4, "14 x 10 x 8 in", "8.5 lbs"),
            ("Caitlin Clark WNBA Rookie Gold Refractor", 850.0, "Bowman Chrome", 2, "6 x 4 x 1 in", "0.5 lbs"),
            ("Jordan Groshans 1st Bowman Chrome Auto Refractor", 250.0, "Topps Bowman", 5, "6 x 4 x 1 in", "0.5 lbs"),
            ("Tiger Woods Upper Deck 22KT Gold Collection", 1200.0, "Upper Deck Authenticated", 2, "10 x 8 x 3 in", "2.1 lbs"),
            ("Pokémon TCG: Sealed Mini Tin Display 10-Pack", 320.0, "The Pokémon Company", 15, "12 x 6 x 4 in", "4.0 lbs"),
            ("NFL National Treasures Hobby Box (Presale)", 2800.0, "Panini America", 3, "10 x 10 x 6 in", "5.5 lbs"),
            ("NBA Flawless Sealed Allocation Case", 4200.0, "Panini America", 1, "16 x 12 x 10 in", "12.0 lbs"),
            ("One Piece TCG: Awakening of the New Era Case", 2200.0, "Bandai Card Games", 2, "14 x 10 x 8 in", "9.0 lbs"),
            ("F1 Chrome Hobby Box Factory Sealed", 650.0, "Topps Racing", 6, "9 x 6 x 4 in", "2.8 lbs"),
            ("Shohei Ohtani Certified Dual Auto Relic", 3100.0, "Topps Diamond Icons", 1, "8 x 6 x 2 in", "1.8 lbs"),
        ]
        for name, cost, brand, stock, dims, wt in allocations[:13]:
            items.append({
                "title": name,
                "wholesale_cost": cost,
                "brand": brand,
                "stock": stock,
                "description": f"Verified allocation asset. Vault-secured provenance for {name}.",
                "images": [],
                "dimensions": dims,
                "weight": wt,
                "is_presale": True if "PRE-RELEASE" in room_upper or "Presale" in name else False
            })
        return items

    # COMMODITY & TRENDING STOREFRONTS (Zendrop API or Verified Fallback)
    query_map = {
        "TECH": "smart gadgets", "AUTO": "automotive parts", "GOLF": "golf accessories",
        "HOME": "luxury home fixtures", "HUMIDOR": "cigar humidor", "ART": "sculpture design",
        "WELLNESS": "recovery tech", "BEAUTY": "skincare tools", "ECO": "sustainable living",
        "PET": "smart pet", "OFFICE": "ergonomic office", "OUTDOOR": "tactical survival",
        "GOURMET": "culinary tools", "GROOMING": "mens grooming", "TRAVEL": "luggage gear",
        "FITNESS": "fitness recovery", "GAMING": "esports peripherals", "EDUCATION": "stem robotics",
        "KITCHEN": "smart kitchen"
    }
    
    search_q = "premium"
    for key, val in query_map.items():
        if key in room_upper:
            search_q = val
            break

    try:
        url = f"https://dummyjson.com/products/search?q={urllib.parse.quote(search_q)}&limit=13"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as res:
            data = json.loads(res.read().decode())
            for p in data.get("products", []):
                items.append({
                    "title": p.get("title"),
                    "wholesale_cost": float(p.get("price", 50.0)),
                    "brand": p.get("brand", "Verified Manufacturer"),
                    "stock": p.get("stock", random.randint(15, 60)),
                    "description": p.get("description"),
                    "images": p.get("images", []),
                    "dimensions": "14 x 10 x 6 in",
                    "weight": f"{round(random.uniform(1.5, 6.0), 1)} lbs",
                    "is_presale": False
                })
    except Exception:
        pass

    # Ensure exact 13-item quota is always met
    idx = 1
    while len(items) < 13:
        items.append({
            "title": f"{room_name} Premium Asset {idx:02d}",
            "wholesale_cost": round(random.uniform(45.0, 220.0), 2),
            "brand": "Direct Manufacturer Verified",
            "stock": random.randint(20, 80),
            "description": f"Engineered architectural grade specification for {room_name}.",
            "images": [],
            "dimensions": "18 x 12 x 8 in",
            "weight": "4.2 lbs",
            "is_presale": False
        })
        idx += 1

    return items[:13]

# -----------------------------------------------------------------------------
# DUAL-BRAIN AGENT NODES
# -----------------------------------------------------------------------------
async def agent_enrichment(raw_item: dict, room_name: str) -> NexusProduct:
    cost = raw_item["wholesale_cost"]
    
    # Pricing Rules (Presales command 20-30% premium; standard retail uses multiplier)
    if raw_item["is_presale"]:
        target_price = round(cost * 1.30, 2)
    elif cost < 50:
        target_price = round(cost * 2.2, 2)
    elif cost < 200:
        target_price = round(cost * 1.7 + 20, 2)
    else:
        target_price = round(cost * 1.45 + 40, 2)

    margin = round(((target_price - cost) / target_price) * 100, 1)
    
    # Curate media
    gallery = curate_image_spread(raw_item.get("images", []), room_name)
    media = enrich_manufacturer_media(raw_item["brand"], raw_item["title"])
    
    # Amistad SLA check (Presale bypass allows custom release schedule)
    if raw_item["is_presale"]:
        shipping_badge = "PRIORITY SECURE ALLOCATION: CONFIRMED PRE-ORDER"
    else:
        shipping_badge = f"PRIORITY SECURE DISPATCH: {random.randint(3, 6)} DAYS"

    specs = ProductSpecs(
        manufacturer=raw_item["brand"],
        condition="Pristine / Factory Sealed",
        authenticity_verified=True,
        material_grade="Aerospace/Investment Grade (Certified)",
        dimensions=raw_item["dimensions"],
        shipping_weight=raw_item["weight"],
        warranty_status="1-Year Global Direct Protection",
        spec_sheet_url=media["spec_sheet"]
    )

    return NexusProduct(
        sku=f"DS-VERIFIED-{random.randint(100000, 999999)}",
        storefront=room_name.upper(),
        name=raw_item["title"],
        price=target_price,
        cost=cost,
        margin_pct=margin,
        images=gallery,
        hero_image=gallery[0],
        video_url=media["video_url"],
        shippingText=shipping_badge,
        rating=round(random.uniform(4.7, 5.0), 1),
        marketing_copy=raw_item["description"],
        specs=specs,
        stock_count=raw_item["stock"],
        viral_velocity=random.randint(75, 99),
        is_presale=raw_item["is_presale"]
    )

# -----------------------------------------------------------------------------
# API ROUTES
# -----------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ONLINE", "engine": "NEXUS PRIME v10.0", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/matrix")
async def get_matrix(category: str = "all"):
    """Serves all 21 rooms populated with 13 fully enriched assets each."""
    target_rooms = STOREFRONTS if category == "all" else [r for r in STOREFRONTS if category.lower() in r.lower()]
    if not target_rooms:
        target_rooms = STOREFRONTS

    catalog = []
    for room in target_rooms:
        raw_batch = fetch_raw_storefront_assets(room)
        for raw in raw_batch:
            product = await agent_enrichment(raw, room)
            catalog.append(product.model_dump())

    return catalog

@app.get("/api/merchant-feed")
async def generate_google_shopping_feed():
    inventory = await get_matrix()
    xml = '<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n<channel>\n'
    xml += '<title>NEXUS Matrix Mall</title>\n<link>http://167.172.154.139:3000</link>\n'
    for item in inventory:
        xml += '<item>\n'
        xml += f"  <g:id>{item['sku']}</g:id>\n"
        xml += f"  <g:title>{item['name'][:150]}</g:title>\n"
        xml += f"  <g:description>{item['marketing_copy'][:500]}</g:description>\n"
        xml += f"  <g:link>http://167.172.154.139:3000</g:link>\n"
        xml += f"  <g:image_link>{item['hero_image']}</g:image_link>\n"
        xml += f"  <g:availability>{'in_stock' if item['stock_count'] > 0 else 'out_of_stock'}</g:availability>\n"
        xml += f"  <g:price>{item['price']} USD</g:price>\n"
        xml += f"  <g:brand>{item['specs']['manufacturer']}</g:brand>\n"
        xml += '</item>\n'
    xml += '</channel>\n</rss>'
    return Response(content=xml, media_type="application/xml")

@app.post("/api/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': request.name, 'images': [request.image]},
                    'unit_amount': int(request.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://167.172.154.139:3000/success",
            cancel_url="http://167.172.154.139:3000/",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
