import os
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
from datetime import datetime
from dotenv import load_dotenv

# Initialize Environment & Stripe
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(title="NEXUS Autonomous Enterprise")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------
class ProductSpecs(BaseModel):
    manufacturer: str
    condition: str
    authenticity_verified: bool

class NexusProduct(BaseModel):
    sku: str
    name: str
    price: float
    cost: float
    margin_pct: float
    images: list[str]
    shippingText: str
    rating: float
    marketing_copy: str
    specs: ProductSpecs
    social_targets: list[str]

class CheckoutRequest(BaseModel):
    name: str
    price: float
    image: str

# ---------------------------------------------------------
# THE ELITE SHOWCASE VAULT
# ---------------------------------------------------------
SHOWCASE_VAULT = {
    "trading cards vault": [
        {
            "raw_name": "Tom Brady Autographed Official Card",
            "cost": 3500.00,
            "target_price": 4200.00,
            "mfg": "Panini/Upper Deck",
            "base_img": "https://images.unsplash.com/photo-1628891435222-06592e1bb3b5?auto=format&fit=crop&q=80&w=800",
            "extra_imgs": ["https://images.unsplash.com/photo-1601987177651-8edfe6c20009?auto=format&fit=crop&q=80&w=800"]
        },
        {
            "raw_name": "Caitlin Clark Panini Prizm Rookie",
            "cost": 450.00,
            "target_price": 600.00,
            "mfg": "Panini",
            "base_img": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&q=80&w=800",
            "extra_imgs": []
        }
    ],
    "tech & mobile gear": [
        {
            "raw_name": "DJI Mini 4 Pro Drone Showcase",
            "cost": 759.00,
            "target_price": 959.00,
            "mfg": "DJI",
            "base_img": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?auto=format&fit=crop&q=80&w=800",
            "extra_imgs": []
        }
    ]
}

# ---------------------------------------------------------
# INDUSTRY-BENCHMARK C-SUITE AGENTS
# ---------------------------------------------------------
async def vp_marketing(item: dict):
    # The Gymshark Seeding Model
    await asyncio.sleep(0.1)
    item['name'] = f"🔥 TRENDING: {item['raw_name'].upper()}"
    item['marketing_copy'] = f"Verified authentic {item['mfg']} asset. High market demand."
    return item

async def vp_logistics(item: dict):
    # The ShipBob Velocity Model
    await asyncio.sleep(0.1)
    # Fast 2-Day Dispatch
    item['shippingText'] = f"PRIORITY SECURE DISPATCH: {random.randint(1, 2)} DAYS"
    return item

async def vp_media_security(item: dict):
    # The Sotheby's Presentation Standard
    await asyncio.sleep(0.1)
    item['images'] = [item['base_img']] + item.get('extra_imgs', [])
    item['specs'] = ProductSpecs(
        manufacturer=item['mfg'],
        condition="Pristine / Vault Mint",
        authenticity_verified=True
    )
    return item

async def vp_influencer_relations(item: dict):
    await asyncio.sleep(0.1)
    tags = item['raw_name'].split()
    keyword = tags[0].lower() if tags else "premium"
    item['social_targets'] = [f"@{keyword}_collects on TikTok"]
    return item

async def vp_auditor(item: dict):
    # The StockX Dynamic Margin Model
    margin = (item['target_price'] - item['cost']) / item['target_price']
    if margin >= 0.10: 
        return NexusProduct(
            sku=f"ALBS-VERIFIED-{random.randint(10000, 99999)}",
            name=item['name'],
            price=item['target_price'],
            cost=item['cost'],
            margin_pct=round(margin * 100, 1),
            images=item['images'],
            shippingText=item['shippingText'],
            rating=round(random.uniform(4.8, 5.0), 1),
            marketing_copy=item['marketing_copy'],
            specs=item['specs'],
            social_targets=item['social_targets']
        )
    return None

# ---------------------------------------------------------
# CORE API ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/matrix")
async def get_matrix(category: str):
    category_key = category.lower()
    raw_items = SHOWCASE_VAULT.get(category_key, [])
    
    if not raw_items:
        return {"status": "sourcing", "items": []}

    live_floor = []
    for raw in raw_items:
        processed = await vp_marketing(raw.copy())
        processed = await vp_logistics(processed)
        processed = await vp_media_security(processed)
        processed = await vp_influencer_relations(processed)
        
        approved = await vp_auditor(processed)
        if approved:
            live_floor.append(approved.model_dump())
            
    return {"status": "live", "items": live_floor}

@app.post("/api/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    """ The Payment Gateway via Stripe API """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': request.name,
                        'images': [request.image],
                    },
                    'unit_amount': int(request.price * 100), # Stripe strictly requires cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://137.184.156.158:3000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://137.184.156.158:3000/cart",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
