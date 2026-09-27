import os
import requests
import stripe
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

raw_stripe = os.getenv("STRIPE_SECRET_KEY", "")
stripe.api_key = raw_stripe.strip() if raw_stripe else ""

ZENDROP_KEY = os.getenv("ZENDROP_API_KEY", "").strip()

class CheckoutItem(BaseModel):
    name: str
    price: float
    image: str

@app.post("/api/checkout")
async def create_checkout_session(item: CheckoutItem):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                        'images': [item.image] if item.image else [],
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://trendingabyss.com/?checkout=success',
            cancel_url='https://trendingabyss.com/',
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

# THE HYBRID IMAGE INJECTOR: Maps secure pictures to each "Room"
CATEGORY_IMAGES = {
    "Trading Cards Vault": "https://images.pokemontcg.io/cel25/15_hires.png",
    "Beauty & Personal Care": "https://images.unsplash.com/photo-1621607512214-68297480165e?w=800",
    "Tech & Mobile Gear": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800",
    "Luxury & Humidor Accessories": "https://images.unsplash.com/photo-1611754026369-0268ecf2fb70?w=800",
    "Golf & Athletic Apparel": "https://images.unsplash.com/photo-1535139262971-c51845709a48?w=800",
    "Home Renovation & Fixtures": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800"
}
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"

def map_supplier_data_to_nexus(raw_api_item):
    wholesale_cost = float(raw_api_item.get('cost', 0.00))
    retail_price = round(wholesale_cost * 1.85, 2)
    
    if retail_price <= 20.00:
        shipping_text = "+ $4.99 Shipping"
        retail_price += 4.99
    elif retail_price <= 50.00 and (retail_price - wholesale_cost) < 15.00:
        shipping_text = "+ $6.99 Shipping"
        retail_price += 6.99
    elif retail_price > 100.00:
        insurance = round(retail_price * 0.015, 2)
        shipping_text = f"FREE Dispatch (+ ${insurance} Vault Insurance)"
        retail_price += insurance
    else:
        shipping_text = "FREE Secure Dispatch"

    storefront_category = str(raw_api_item.get('category', 'Tech & Mobile Gear'))
    
    # OVERRIDE BROKEN ZENDROP IMAGES WITH OUR SECURE HARDCODED LINKS
    hero_img = CATEGORY_IMAGES.get(storefront_category, DEFAULT_IMAGE)
    
    return {
        "sku": str(raw_api_item.get('sku', f"DS-VERIFIED-{str(id(raw_api_item))[-6:]}")),
        "name": str(raw_api_item.get('title', 'Verified Manufacturer Asset')),
        "price": round(retail_price, 2),
        "stock_count": int(raw_api_item.get('inventory_quantity', random.randint(3, 24))),
        "hero_image": hero_img,
        "images": [hero_img],
        "shippingText": shipping_text,
        "storefront": storefront_category,
        "specs": {
            "manufacturer": str(raw_api_item.get('brand', 'Direct Manufacturer')),
            "condition": "Pristine / Factory Sealed"
        }
    }

@app.get("/api/matrix")
async def get_matrix():
    if not ZENDROP_KEY:
        return []

    try:
        # THE STEALTH BYPASS DISGUISE (Restored from your original code)
        headers = {
            "Authorization": f"Bearer {ZENDROP_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get("https://api.zendrop.com/v1/products", headers=headers, timeout=15)
        
        if response.status_code != 200:
             return []

        live_items = response.json().get('data', [])
        
        if not live_items:
             return []

        inventory = []
        for raw_item in live_items:
            # We no longer skip items if Zendrop's images are missing, because we are supplying our own!
            if int(raw_item.get('inventory_quantity', 0)) <= 0:
                continue
            inventory.append(map_supplier_data_to_nexus(raw_item))
            
        return inventory
        
    except Exception as e:
        return []
