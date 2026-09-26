from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import stripe
import os
import requests
import random

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
            success_url='http://167.172.154.139:3000/?checkout=success',
            cancel_url='http://167.172.154.139:3000/?checkout=canceled',
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

def map_supplier_data_to_nexus(raw_api_item):
    wholesale_cost = float(raw_api_item.get('cost', 0.00))
    retail_price = round(wholesale_cost * 1.85, 2)
    shipping_text = "Standard Dispatch"
    
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

    raw_images = raw_api_item.get('images', [])
    hero_img = raw_images[0] if len(raw_images) > 0 else "https://via.placeholder.com/800x800.png?text=IMAGE+SYNCING"
    
    return {
        "sku": str(raw_api_item.get('sku', f"DS-VERIFIED-{str(id(raw_api_item))[-6:]}")),
        "name": str(raw_api_item.get('title', 'Verified Manufacturer Asset')),
        "price": round(retail_price, 2),
        "stock_count": int(raw_api_item.get('inventory_quantity', random.randint(3, 24))),
        "hero_image": str(hero_img),
        "images": raw_images,
        "video_url": raw_api_item.get('video_url', None),
        "shippingText": shipping_text,
        "storefront": str(raw_api_item.get('category', 'Trading Cards Vault')),
        "specs": {
            "manufacturer": str(raw_api_item.get('brand', 'Direct Manufacturer')),
            "condition": "Pristine / Factory Sealed",
            "material_grade": str(raw_api_item.get('material', 'Commercial Grade')),
            "dimensions": str(raw_api_item.get('dimensions', 'Verified Specs Available')),
            "shipping_weight": str(raw_api_item.get('weight', 'Calculated at dispatch')),
            "warranty_status": "Active Manufacturer Guarantee"
        }
    }

@app.get("/api/matrix")
async def get_matrix():
    return [
        {
            "sku": "DS-TEST-001",
            "name": "TEST ASSET: RENDER CONNECTION LIVE",
            "price": 199.99,
            "stock_count": 42,
            "hero_image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
            "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"],
            "shippingText": "System Diagnostic Mode",
            "storefront": "Tech & Mobile Gear",
            "specs": {
                "manufacturer": "NEXUS Core",
                "status": "Diagnostic Override Active"
            }
        },
        {
            "sku": "DS-TEST-002",
            "name": "TEST ASSET: HEALTH MODULE LIVE",
            "price": 45.00,
            "stock_count": 12,
            "hero_image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800",
            "images": ["https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800"],
            "shippingText": "System Diagnostic Mode",
            "storefront": "Health & Wellness Tech",
            "specs": {
                "manufacturer": "NEXUS Core",
                "status": "Diagnostic Override Active"
            }
        }
    ]
