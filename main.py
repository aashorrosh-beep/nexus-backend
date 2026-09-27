import os
import stripe
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

@app.get("/api/matrix")
async def get_matrix():
    # SECURE VISUAL FALLBACK CATALOG - BYPASSING ZENDROP API BLOCK
    return [
        {
            "sku": "NX-TCG-001",
            "name": "Pokemon 30th Celebration Ultra-Premium Collection",
            "price": 549.95,
            "stock_count": 8,
            "hero_image": "https://images.pokemontcg.io/cel25/15_hires.png",
            "images": ["https://images.pokemontcg.io/cel25/15_hires.png"],
            "shippingText": "FREE Secure Vault Dispatch",
            "storefront": "Trading Cards Vault",
            "specs": {"manufacturer": "The Pokemon Company", "condition": "Factory Sealed"}
        },
        {
            "sku": "NX-MENS-020",
            "name": "Premium Men's Grooming Kit",
            "price": 17.16,
            "stock_count": 45,
            "hero_image": "https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=800&q=80",
            "images": ["https://images.unsplash.com/photo-1621607512214-68297480165e?auto=format&fit=crop&w=800&q=80"],
            "shippingText": "FREE Express Shipping",
            "storefront": "Beauty & Personal Care",
            "specs": {"brand": "Direct Manufacturer Verified", "condition": "Pristine / Factory Sealed", "authentication": "Verified Direct"}
        },
        {
            "sku": "NX-TECH-001",
            "name": "Nexus Core Hardware Node",
            "price": 199.99,
            "stock_count": 15,
            "hero_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
            "images": ["https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"],
            "shippingText": "FREE Dispatch",
            "storefront": "Tech & Mobile Gear",
            "specs": {"manufacturer": "Nexus Systems", "condition": "New"}
        },
        {
            "sku": "NX-HOME-001",
            "name": "Luxury Home Humidor Setup",
            "price": 249.99,
            "stock_count": 12,
            "hero_image": "https://images.unsplash.com/photo-1611754026369-0268ecf2fb70?w=800",
            "images": ["https://images.unsplash.com/photo-1611754026369-0268ecf2fb70?w=800"],
            "shippingText": "FREE Vault Delivery",
            "storefront": "Luxury & Humidor Accessories",
            "specs": {"manufacturer": "Premium Woods", "condition": "Pristine"}
        }
    ]
