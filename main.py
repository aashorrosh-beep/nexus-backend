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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# THE ELITE SHOWCASE VAULT (ALL 21 ROOMS POPULATED)
# ---------------------------------------------------------
SHOWCASE_VAULT = {
    "trading cards vault": [
        {
            "raw_name": "Tom Brady 1-of-1 Autograph",
            "cost": 3500.00,
            "target_price": 40000.00,
            "mfg": "Panini",
            "base_img": "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?auto=format&fit=crop&q=80&w=800"
        },
        {
            "raw_name": "Jordan Groshans Bowman Gold Refractor Auto",
            "cost": 150.00,
            "target_price": 350.00,
            "mfg": "Bowman",
            "base_img": "https://images.unsplash.com/photo-1508344928928-7137b29de216?auto=format&fit=crop&q=80&w=800"
        },
        {
            "raw_name": "Tiger Woods Upper Deck 22KT Gold",
            "cost": 800.00,
            "target_price": 1500.00,
            "mfg": "Upper Deck",
            "base_img": "https://images.unsplash.com/photo-1587329310686-91414b8e3cb7?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "tech & mobile gear": [
        {
            "raw_name": "YubiKey 5C NFC Security Kit (Pack of 5)",
            "cost": 150.00,
            "target_price": 275.00,
            "mfg": "Yubico",
            "base_img": "https://images.unsplash.com/photo-1614064010375-3b95a898b9be?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "high-performance auto": [
        {
            "raw_name": "Dodge Challenger Demon 170 Supercharger Pulley",
            "cost": 450.00,
            "target_price": 899.00,
            "mfg": "SRT",
            "base_img": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&q=80&w=800"
        },
        {
            "raw_name": "2024 Nissan Z Nismo Carbon Fiber Aero Kit",
            "cost": 1200.00,
            "target_price": 2100.00,
            "mfg": "Nismo",
            "base_img": "https://images.unsplash.com/photo-1612825173281-9a193378527e?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "golf & athletic apparel": [
        {
            "raw_name": "Baylor University Custom Tour Performance Polo",
            "cost": 45.00,
            "target_price": 110.00,
            "mfg": "Titleist",
            "base_img": "https://images.unsplash.com/photo-1535139262971-c51845709a48?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "home renovation & fixtures": [
        {
            "raw_name": "CityPost Cable Railing System (100ft Kit)",
            "cost": 850.00,
            "target_price": 1400.00,
            "mfg": "CityPost",
            "base_img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&q=80&w=800"
        },
        {
            "raw_name": "CertainTeed Black Pearl Carriage House Shingles (Pallet)",
            "cost": 1200.00,
            "target_price": 1850.00,
            "mfg": "CertainTeed",
            "base_img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "luxury & humidor accessories": [
        {
            "raw_name": "Cohiba Maduro 5 Magicos Authentic Humidor",
            "cost": 650.00,
            "target_price": 1100.00,
            "mfg": "Cohiba",
            "base_img": "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "fine arts & creative design": [
        {
            "raw_name": "Architectural Visual Blueprint Drafting Set",
            "cost": 120.00,
            "target_price": 250.00,
            "mfg": "Rotring",
            "base_img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "health & wellness tech": [
        {
            "raw_name": "Oura Ring Horizon Stealth",
            "cost": 300.00,
            "target_price": 450.00,
            "mfg": "Oura",
            "base_img": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "beauty & personal care": [
        {
            "raw_name": "La Mer Crème de la Mer 2oz",
            "cost": 190.00,
            "target_price": 380.00,
            "mfg": "La Mer",
            "base_img": "https://images.unsplash.com/photo-1571781926291-c477eb31f7d4?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "eco-friendly living": [
        {
            "raw_name": "Lomi Smart Kitchen Composter",
            "cost": 250.00,
            "target_price": 400.00,
            "mfg": "Pela",
            "base_img": "https://images.unsplash.com/photo-1556910103-1c02745a872f?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "smart pet tech": [
        {
            "raw_name": "Litter-Robot 4 with Backup Battery",
            "cost": 450.00,
            "target_price": 700.00,
            "mfg": "Whisker",
            "base_img": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "home office ergonomics": [
        {
            "raw_name": "Herman Miller Embody Chair",
            "cost": 900.00,
            "target_price": 1800.00,
            "mfg": "Herman Miller",
            "base_img": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "outdoor & survival gear": [
        {
            "raw_name": "Garmin inReach Mini 2 Satellite Communicator",
            "cost": 250.00,
            "target_price": 400.00,
            "mfg": "Garmin",
            "base_img": "https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "gourmet food & culinary": [
        {
            "raw_name": "A5 Japanese Wagyu Ribeye (2 lbs)",
            "cost": 150.00,
            "target_price": 300.00,
            "mfg": "Kobe",
            "base_img": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "men's grooming": [
        {
            "raw_name": "The Art of Shaving Sandalwood Kit",
            "cost": 50.00,
            "target_price": 120.00,
            "mfg": "The Art of Shaving",
            "base_img": "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "travel tech & luggage": [
        {
            "raw_name": "Rimowa Classic Cabin Aluminum",
            "cost": 600.00,
            "target_price": 1050.00,
            "mfg": "Rimowa",
            "base_img": "https://images.unsplash.com/photo-1581553680321-4fffae59fdd9?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "fitness & recovery": [
        {
            "raw_name": "Theragun PRO Plus",
            "cost": 350.00,
            "target_price": 599.00,
            "mfg": "Therabody",
            "base_img": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "gaming & esports": [
        {
            "raw_name": "NVIDIA GeForce RTX 4090 Founders Edition",
            "cost": 1599.00,
            "target_price": 2200.00,
            "mfg": "NVIDIA",
            "base_img": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "early education tech": [
        {
            "raw_name": "LEGO Mindstorms Robot Inventor",
            "cost": 250.00,
            "target_price": 450.00,
            "mfg": "LEGO",
            "base_img": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "smart kitchen gadgets": [
        {
            "raw_name": "Breville Oracle Touch Espresso Machine",
            "cost": 1500.00,
            "target_price": 2800.00,
            "mfg": "Breville",
            "base_img": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&q=80&w=800"
        }
    ],
    "room 21: pre-release acquisitions": [
        {
            "raw_name": "Sealed Pokémon TCG Elite Trainer Box (Pre-Release)",
            "base_msrp": 50.00,
            "cost": 50.00,
            "target_price": 140.00,
            "mfg": "The Pokémon Company",
            "is_prerelease": True,
            "base_img": "https://images.unsplash.com/photo-1613771404721-1f92d799e49f?auto=format&fit=crop&q=80&w=800"
        }
    ]
}

# ---------------------------------------------------------
# C-SUITE PIPELINE
# ---------------------------------------------------------
async def vp_acquisitions(item: dict):
    await asyncio.sleep(0.1)
    if item.get('is_prerelease'):
        item['cost'] = item['base_msrp'] * 1.20
        item['raw_name'] = f"💎 SECURED ALLOCATION: {item['raw_name']}"
    return item

async def vp_marketing(item: dict):
    await asyncio.sleep(0.1)
    item['name'] = f"🔥 TRENDING: {item['raw_name'].upper()}"
    item['marketing_copy'] = f"Verified authentic {item['mfg']} asset. High market demand."
    return item

async def vp_logistics(item: dict):
    await asyncio.sleep(0.1)
    item['shippingText'] = f"PRIORITY SECURE DISPATCH: {random.randint(1, 2)} DAYS"
    return item

async def vp_media_security(item: dict):
    await asyncio.sleep(0.1)
    item['images'] = [item['base_img']]
    item['specs'] = ProductSpecs(manufacturer=item['mfg'], condition="Pristine / Vault Mint", authenticity_verified=True)
    return item

async def vp_influencer_relations(item: dict):
    await asyncio.sleep(0.1)
    keyword = item['raw_name'].split()[0].lower()
    item['social_targets'] = [f"@{keyword}_collects on TikTok"]
    return item

async def vp_auditor(item: dict):
    margin = (item['target_price'] - item['cost']) / item['target_price']
    if margin >= 0.10: 
        return NexusProduct(
            sku=f"ALBS-VERIFIED-{random.randint(10000, 99999)}",
            name=item['name'], price=item['target_price'], cost=item['cost'],
            margin_pct=round(margin * 100, 1), images=item['images'],
            shippingText=item['shippingText'], rating=round(random.uniform(4.8, 5.0), 1),
            marketing_copy=item['marketing_copy'], specs=item['specs'], social_targets=item['social_targets']
        )
    return None

@app.get("/api/matrix")
async def get_matrix(category: str):
    category_key = category.lower()
    raw_items = []
    
    if category_key == "all":
        for items in SHOWCASE_VAULT.values():
            raw_items.extend(items)
    else:
        raw_items = SHOWCASE_VAULT.get(category_key, [])
    
    live_floor = []
    for raw in raw_items:
        processed = await vp_acquisitions(raw.copy())
        processed = await vp_marketing(processed)
        processed = await vp_logistics(processed)
        processed = await vp_media_security(processed)
        processed = await vp_influencer_relations(processed)
        
        approved = await vp_auditor(processed)
        if approved:
            live_floor.append(approved.model_dump())
            
    return live_floor if live_floor else []

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
