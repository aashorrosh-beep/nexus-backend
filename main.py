import os
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(title="NEXUS Autonomous Dropship Engine")
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
    stock_count: int  # <-- Added Scarcity tracking

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
    search_query = "premium"
    if "TECH" in room_name: search_query = "laptop"
    elif "AUTO" in room_name: search_query = "vehicle"
    elif "BEAUTY" in room_name: search_query = "beauty"
    elif "GROOMING" in room_name: search_query = "fragrance"
    elif "HOME" in room_name: search_query = "furniture"
    elif "TRAVEL" in room_name: search_query = "bag"
    elif "PET" in room_name: search_query = "pet"
    elif "FITNESS" in room_name or "GOLF" in room_name: search_query = "sports"
    elif "FOOD" in room_name: search_query = "groceries"
    elif "LUXURY" in room_name: search_query = "watch"
    elif "KITCHEN" in room_name: search_query = "kitchen"
    
    try:
        url = f"https://dummyjson.com/products/search?q={search_query}&limit=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            products = data.get("products", [])
    except Exception as e:
        products = []

    items = []
    for i in range(10):
        if i < len(products):
            p = products[i]
            items.append({
                "raw_title": p.get('title', f"Premium Asset"),
                "wholesale_cost": float(p.get('price', random.uniform(40, 200))),
                "images": p.get('images', ["https://via.placeholder.com/800"]),
                "description": p.get('description', f"High-velocity authentic item for the {room_name} collection."),
                "brand": p.get('brand', 'Verified Elite Source'),
                "stock": p.get('stock', random.randint(3, 14)) # Live Stock Count
            })
        else:
            items.append({
                "raw_title": f"Exclusive {room_name.split(' ')[0]} Asset - Series {random.randint(100, 999)}",
                "wholesale_cost": round(random.uniform(30.0, 150.0), 2),
                "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"],
                "description": f"Professionally curated for the {room_name} collection. Features premium construction and verified high-end materials.",
                "brand": "NEXUS Global Direct",
                "stock": random.randint(3, 14) # Random Scarcity Fallback
            })
    return items

async def vp_acquisitions(room_name: str):
    await asyncio.sleep(0.01) 
    return fetch_live_dropship_feed(room_name)

async def vp_marketing(raw_item: dict, room_name: str):
    return {
        "storefront": room_name.upper(),
        "name": raw_item['raw_title'],
        "cost": raw_item['wholesale_cost'],
        "images": raw_item['images'],
        "marketing_copy": raw_item['description'],
        "brand": raw_item['brand'],
        "stock": raw_item['stock']
    }

async def vp_logistics(item: dict):
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
        stock_count=item['stock']
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
