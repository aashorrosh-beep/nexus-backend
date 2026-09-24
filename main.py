import os
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(title="NEXUS Autonomous Enterprise")
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
    social_targets: list[str]

class CheckoutRequest(BaseModel):
    name: str
    price: float
    image: str

# ---------------------------------------------------------
# TRUE GLOBAL TRENDING VAULT (THE 21 DOORS)
# ---------------------------------------------------------
SHOWCASE_VAULT = {
    "trading cards vault": [
        {"raw_name": "Tom Brady 1-of-1 Autograph", "cost": 3500.00, "target_price": 40000.00, "mfg": "Panini", "base_img": "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?auto=format&fit=crop&q=80&w=800"},
        {"raw_name": "Charizard Base Set 1st Edition PSA 10", "cost": 150000.00, "target_price": 220000.00, "mfg": "Wizards of the Coast", "base_img": "https://images.unsplash.com/photo-1613771404721-1f92d799e49f?auto=format&fit=crop&q=80&w=800"}
    ],
    "tech & mobile gear": [
        {"raw_name": "Apple Vision Pro 1TB", "cost": 3899.00, "target_price": 4500.00, "mfg": "Apple", "base_img": "https://images.unsplash.com/photo-1614064010375-3b95a898b9be?auto=format&fit=crop&q=80&w=800"}
    ],
    "high-performance auto": [
        {"raw_name": "Porsche GT3 RS Carbon Steering Wheel", "cost": 1800.00, "target_price": 3200.00, "mfg": "Porsche", "base_img": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&q=80&w=800"}
    ],
    "golf & athletic apparel": [
        {"raw_name": "Nike Air Jordan 1 Low G", "cost": 140.00, "target_price": 280.00, "mfg": "Nike", "base_img": "https://images.unsplash.com/photo-1535139262971-c51845709a48?auto=format&fit=crop&q=80&w=800"}
    ],
    "home renovation & fixtures": [
        {"raw_name": "Philips Hue Smart Lighting Hub Bundle", "cost": 199.00, "target_price": 350.00, "mfg": "Philips", "base_img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&q=80&w=800"}
    ],
    "luxury & humidor accessories": [
        {"raw_name": "Elie Bleu Alba 75 Cigar Humidor", "cost": 2100.00, "target_price": 3400.00, "mfg": "Elie Bleu", "base_img": "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&q=80&w=800"}
    ],
    "fine arts & creative design": [
        {"raw_name": "Wacom Cintiq Pro 27", "cost": 3499.00, "target_price": 4200.00, "mfg": "Wacom", "base_img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&q=80&w=800"}
    ],
    "health & wellness tech": [
        {"raw_name": "Eight Sleep Pod 4 Cover", "cost": 2195.00, "target_price": 2800.00, "mfg": "Eight Sleep", "base_img": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&q=80&w=800"}
    ],
    "beauty & personal care": [
        {"raw_name": "Dyson Airwrap Multi-Styler Complete", "cost": 599.00, "target_price": 850.00, "mfg": "Dyson", "base_img": "https://images.unsplash.com/photo-1571781926291-c477eb31f7d4?auto=format&fit=crop&q=80&w=800"}
    ],
    "eco-friendly living": [
        {"raw_name": "Bambu Lab X1-Carbon Combo 3D Printer", "cost": 1449.00, "target_price": 2100.00, "mfg": "Bambu Lab", "base_img": "https://images.unsplash.com/photo-1556910103-1c02745a872f?auto=format&fit=crop&q=80&w=800"}
    ],
    "smart pet tech": [
        {"raw_name": "Litter-Robot 4 with Backup Battery", "cost": 699.00, "target_price": 950.00, "mfg": "Whisker", "base_img": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&q=80&w=800"}
    ],
    "home office ergonomics": [
        {"raw_name": "Herman Miller Aeron Onyx", "cost": 1805.00, "target_price": 2300.00, "mfg": "Herman Miller", "base_img": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800"}
    ],
    "outdoor & survival gear": [
        {"raw_name": "Garmin Fenix 8 Pro Sapphire", "cost": 999.00, "target_price": 1400.00, "mfg": "Garmin", "base_img": "https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&q=80&w=800"}
    ],
    "gourmet food & culinary": [
        {"raw_name": "Ooni Karu 16 Multi-Fuel Pizza Oven", "cost": 799.00, "target_price": 1100.00, "mfg": "Ooni", "base_img": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&q=80&w=800"}
    ],
    "men's grooming": [
        {"raw_name": "Manscaped Platinum Package 5.0", "cost": 139.00, "target_price": 220.00, "mfg": "Manscaped", "base_img": "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&q=80&w=800"}
    ],
    "travel tech & luggage": [
        {"raw_name": "Rimowa Original Cabin Silver", "cost": 1430.00, "target_price": 1900.00, "mfg": "Rimowa", "base_img": "https://images.unsplash.com/photo-1581553680321-4fffae59fdd9?auto=format&fit=crop&q=80&w=800"}
    ],
    "fitness & recovery": [
        {"raw_name": "Theragun PRO Plus Smart Percussive", "cost": 599.00, "target_price": 850.00, "mfg": "Therabody", "base_img": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&q=80&w=800"}
    ],
    "gaming & esports": [
        {"raw_name": "Sony PlayStation 5 Pro (Pre-Order Allocation)", "cost": 699.00, "target_price": 1200.00, "mfg": "Sony", "base_img": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&q=80&w=800"}
    ],
    "early education tech": [
        {"raw_name": "Meta Quest 3 Educational Immersive Kit", "cost": 499.00, "target_price": 750.00, "mfg": "Meta", "base_img": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?auto=format&fit=crop&q=80&w=800"}
    ],
    "smart kitchen gadgets": [
        {"raw_name": "Breville Barista Touch Impress", "cost": 1499.00, "target_price": 2100.00, "mfg": "Breville", "base_img": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&q=80&w=800"}
    ],
    "room 21: pre-release acquisitions": [
        {"raw_name": "NVIDIA RTX 5090 Founders Edition (Secured Allocation)", "base_msrp": 1999.00, "cost": 1999.00, "target_price": 3800.00, "mfg": "NVIDIA", "is_prerelease": True, "base_img": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&q=80&w=800"}
    ]
}

# ---------------------------------------------------------
# C-SUITE PIPELINE
# ---------------------------------------------------------
async def vp_acquisitions(item: dict):
    await asyncio.sleep(0.05)
    if item.get('is_prerelease'):
        item['cost'] = item['base_msrp'] * 1.20
        item['raw_name'] = f"💎 SECURED ALLOCATION: {item['raw_name']}"
    return item

async def vp_marketing(item: dict):
    await asyncio.sleep(0.05)
    item['name'] = f"🔥 TRENDING: {item['raw_name'].upper()}"
    item['marketing_copy'] = f"Verified authentic {item['mfg']} global market asset. High consumer demand velocity."
    return item

async def vp_logistics(item: dict):
    await asyncio.sleep(0.05)
    item['shippingText'] = f"PRIORITY SECURE DISPATCH: {random.randint(1, 2)} DAYS"
    return item

async def vp_media_security(item: dict):
    await asyncio.sleep(0.05)
    item['images'] = [item['base_img']]
    item['specs'] = ProductSpecs(manufacturer=item['mfg'], condition="Pristine / Vault Mint", authenticity_verified=True)
    return item

async def vp_influencer_relations(item: dict):
    await asyncio.sleep(0.05)
    item['social_targets'] = [f"@{item['mfg'].lower().replace(' ', '')}_global on TikTok"]
    return item

async def vp_auditor(item: dict):
    margin = (item['target_price'] - item['cost']) / item['target_price']
    if margin >= 0.10: 
        return NexusProduct(
            sku=f"ALBS-VERIFIED-{random.randint(10000, 99999)}",
            storefront=item['storefront'], 
            name=item['name'], price=item['target_price'], cost=item['cost'],
            margin_pct=round(margin * 100, 1), images=item['images'],
            shippingText=item['shippingText'], rating=round(random.uniform(4.8, 5.0), 1),
            marketing_copy=item['marketing_copy'], specs=item['specs'], social_targets=item['social_targets']
        )
    return None

@app.get("/api/matrix")
async def get_matrix(category: str):
    live_floor = []
    for room_name, raw_list in SHOWCASE_VAULT.items():
        for raw in raw_list:
            raw_copy = raw.copy()
            raw_copy['storefront'] = room_name.upper()
            processed = await vp_acquisitions(raw_copy)
            processed = await vp_marketing(processed)
            processed = await vp_logistics(processed)
            processed = await vp_media_security(processed)
            processed = await vp_influencer_relations(processed)
            
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
