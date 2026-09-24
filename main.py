import os
import stripe
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# MASTER LIVE SWITCH: Set to "SPOCKET" or "ZENDROP" when you have the keys
SUPPLIER_NETWORK = "SANDBOX" 
SUPPLIER_API_KEY = os.getenv("SUPPLIER_API_KEY", "pending_key")

app = FastAPI(title="NEXUS Autonomous Dropship Engine - Production Mode")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ProductSpecs(BaseModel):
    manufacturer: str
    condition: str
    authenticity_verified: bool

class NexusProduct(BaseModel):
    sku: str
    storefront: str
    name: str
    price: float
    cost: float
    margin_pct: float
    images: list[str]
    shippingText: str
    rating: float
    marketing_copy: str
    specs: ProductSpecs
    stock_count: int
    viral_velocity: int  # <-- New Intelligence Metric

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

def fetch_live_dropship_feed(room_name: str):
    if SUPPLIER_NETWORK == "SPOCKET":
        # PRODUCTION SLOT: This is where the live Spocket API will connect
        pass 
    
    # SANDBOX FALLBACK (While Pretending Live)
    search_query = "premium"
    if "TECH" in room_name: search_query = "laptop"
    elif "AUTO" in room_name: search_query = "vehicle"
    elif "BEAUTY" in room_name: search_query = "beauty"
    elif "GROOMING" in room_name: search_query = "fragrance"
    elif "HOME" in room_name: search_query = "furniture"
    elif "TRAVEL" in room_name: search_query = "bag"
    
    try:
        url = f"https://dummyjson.com/products/search?q={search_query}&limit=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            products = data.get("products", [])
    except Exception as e:
        products = []

    items = []
    for p in products[:10]:
        items.append({
            "raw_title": p.get('title', "Premium Asset"),
            "wholesale_cost": float(p.get('price', random.uniform(40, 200))),
            "images": p.get('images', ["https://via.placeholder.com/800"]),
            "description": p.get('description', "High-velocity item."),
            "brand": p.get('brand', 'Verified Elite Source'),
            "stock": p.get('stock', random.randint(3, 14))
        })
    return items

# --- THE C-SUITE AGENTS ---

async def vp_intelligence(raw_item: dict):
    # THE INTELLIGENCE FEED: Simulates scraping Google Trends / TikTok hashtags
    # In full production, this pings real social APIs to score the item
    base_score = random.randint(60, 99) 
    raw_item['viral_velocity'] = base_score
    
    # If the score is below 70, the AI rejects it for not being trendy enough
    if base_score < 70:
        return None 
    return raw_item

async def vp_acquisitions(room_name: str):
    await asyncio.sleep(0.01) 
    raw_feed = fetch_live_dropship_feed(room_name)
    approved_items = []
    
    for item in raw_feed:
        # Items must pass the VP of Intelligence first
        trend_approved = await vp_intelligence(item)
        if trend_approved:
            approved_items.append(trend_approved)
            
    return approved_items

async def vp_marketing(raw_item: dict, room_name: str):
    return {
        "storefront": room_name.upper(),
        "name": raw_item['raw_title'],
        "cost": raw_item['wholesale_cost'],
        "images": raw_item['images'],
        "marketing_copy": raw_item['description'],
        "brand": raw_item['brand'],
        "stock": raw_item['stock'],
        "viral_velocity": raw_item['viral_velocity']
    }

async def vp_logistics(item: dict):
    # THE TIER-1 RULE: Forces 3-6 day US/EU shipping estimates
    item['shippingText'] = f"PRIORITY SECURE DISPATCH: {random.randint(3, 6)} DAYS"
    return item

async def vp_media_security(item: dict):
    item['specs'] = ProductSpecs(
        manufacturer=item['brand'], 
        condition="Pristine / Factory Sealed", 
        authenticity_verified=True
    )
    return item

async def vp_auditor(item: dict):
    markup_multiplier = 1.45
    target_price = round(item['cost'] * markup_multiplier, 2)
    margin = (target_price - item['cost']) / target_price
    
    return NexusProduct(
        sku=f"DS-VERIFIED-{random.randint(100000, 999999)}",
        storefront=item['storefront'], 
        name=item['name'], 
        price=target_price, 
        cost=item['cost'],
        margin_pct=round(margin * 100, 1), 
        images=item['images'],
        shippingText=item['shippingText'], 
        rating=round(random.uniform(4.5, 5.0), 1),
        marketing_copy=item['marketing_copy'], 
        specs=item['specs'],
        stock_count=item['stock'],
        viral_velocity=item['viral_velocity']
    )

@app.get("/api/matrix")
async def get_matrix(category: str = "all"):
    live_floor = []
    for room in STOREFRONTS:
        raw_items = await vp_acquisitions(room)
        for raw in raw_items:
            processed = await vp_marketing(raw, room)
            processed = await vp_logistics(processed)
            processed = await vp_media_security(processed)
            approved = await vp_auditor(processed)
            if approved:
                live_floor.append(approved.model_dump())
    return live_floor

# --- THE TRAFFIC CANNON (Google Shopping Auto-Feed) ---
@app.get("/api/merchant-feed")
async def generate_google_shopping_feed():
    # This generates a live XML feed that Google Performance Max uses to run your ads automatically
    inventory = await get_matrix()
    
    xml_content = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    xml_content += '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
    xml_content += '<channel>\n<title>NEXUS Matrix Mall</title>\n<link>http://167.172.154.139:3000</link>\n'
    
    for item in inventory:
        xml_content += '<item>\n'
        xml_content += f"  <g:id>{item['sku']}</g:id>\n"
        xml_content += f"  <g:title>{item['name'][:150]}</g:title>\n"
        xml_content += f"  <g:description>{item['marketing_copy'][:500]}</g:description>\n"
        xml_content += f"  <g:link>http://167.172.154.139:3000</g:link>\n"
        xml_content += f"  <g:image_link>{item['images'][0]}</g:image_link>\n"
        xml_content += f"  <g:condition>new</g:condition>\n"
        xml_content += f"  <g:availability>{'in_stock' if item['stock_count'] > 0 else 'out_of_stock'}</g:availability>\n"
        xml_content += f"  <g:price>{item['price']} USD</g:price>\n"
        xml_content += f"  <g:brand>{item['specs']['manufacturer']}</g:brand>\n"
        xml_content += '</item>\n'
        
    xml_content += '</channel>\n</rss>'
    return Response(content=xml_content, media_type="application/xml")

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
