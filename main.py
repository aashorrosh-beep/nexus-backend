import os
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
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

class CheckoutRequest(BaseModel):
    name: str
    price: float
    image: str

# --- THE 21 STOREFRONTS ---
STOREFRONTS = [
    "Trading Cards Vault", "Tech & Mobile Gear", "High-Performance Auto", "Golf & Athletic Apparel",
    "Home Renovation & Fixtures", "Luxury & Humidor Accessories", "Fine Arts & Creative Design",
    "Health & Wellness Tech", "Beauty & Personal Care", "Eco-Friendly Living", "Smart Pet Tech",
    "Home Office Ergonomics", "Outdoor & Survival Gear", "Gourmet Food & Culinary", "Men's Grooming",
    "Travel Tech & Luggage", "Fitness & Recovery", "Gaming & Esports", "Early Education Tech",
    "Smart Kitchen Gadgets", "Room 21: Pre-Release Acquisitions"
]

# --- SIMULATED LIVE DROPSHIP API FEED ---
def fetch_live_dropship_feed(room_name: str):
    items = []
    for i in range(1, 11):
        raw_cost = round(random.uniform(15.0, 150.0), 2)
        items.append({
            "raw_title": f"2026 Trending {room_name} Item {i} High Quality Fast Ship Wholesale",
            "wholesale_cost": raw_cost,
            "supplier_origin": random.choice(["US Warehouse", "Global Hub"]),
            "base_img": f"https://picsum.photos/seed/{room_name.replace(' ', '')}{i}/800/800"
        })
    return items

# --- C-SUITE PIPELINE ---
async def vp_acquisitions(room_name: str):
    await asyncio.sleep(0.01) 
    return fetch_live_dropship_feed(room_name)

async def vp_marketing(raw_item: dict, room_name: str):
    # Generates a realistic product name model instead of generic "Asset 1"
    model_num = random.randint(100, 999)
    return {
        "storefront": room_name.upper(),
        "name": f"{room_name.split(' ')[0]} Elite Series - Model {model_num}X",
        "cost": raw_item['wholesale_cost'],
        "base_img": raw_item['base_img'],
        "marketing_copy": f"Professionally curated for the {room_name} collection with guaranteed high-velocity demand and premium construction."
    }

async def vp_logistics(item: dict):
    # Changed from Dropship to Priority Dispatch
    item['shippingText'] = f"PRIORITY SECURE DISPATCH: {random.randint(3, 6)} DAYS"
    return item

async def vp_media_security(item: dict):
    item['images'] = [item['base_img']]
    item['specs'] = ProductSpecs(
        manufacturer="Curated Elite Brands", 
        condition="Pristine / Factory Sealed", 
        authenticity_verified=True
    )
    return item

async def vp_auditor(item: dict):
    # Enforces a strict 45% retail markup strategy
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
        specs=item['specs']
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
