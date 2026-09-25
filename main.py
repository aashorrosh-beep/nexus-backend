from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import stripe
import os
import random

# This is the line that was missing - it boots the server
app = FastAPI()

# Allow your DigitalOcean frontend to talk to this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connects to the sk_live_ key you set in Render Environment Variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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

# The new Dynamic Margin & Payload Mapper
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
        "sku": raw_api_item.get('sku', f"DS-VERIFIED-{str(id(raw_api_item))[-6:]}"),
        "name": raw_api_item.get('title', 'Verified Manufacturer Asset'),
        "price": round(retail_price, 2),
        "stock_count": raw_api_item.get('inventory_quantity', random.randint(3, 24)),
        "hero_image": hero_img,
        "images": raw_images,
        "video_url": raw_api_item.get('video_url', None),
        "shippingText": shipping_text,
        "storefront": raw_api_item.get('category', 'Trading Cards Vault'),
        "specs": {
            "manufacturer": raw_api_item.get('brand', 'Direct Manufacturer Verified'),
            "condition": "Pristine / Factory Sealed",
            "material_grade": raw_api_item.get('material', 'Commercial Grade'),
            "dimensions": raw_api_item.get('dimensions', 'Data syncing...'),
            "shipping_weight": raw_api_item.get('weight', 'Calculated at dispatch'),
            "warranty_status": "Active Manufacturer Guarantee"
        }
    }

@app.get("/api/matrix")
async def get_matrix():
    inventory = []
    storefronts = [
        "Room 22: Squishmallows & Blind Boxes", "Room 21: Pre-Release Acquisitions", "Trading Cards Vault", 
        "Tech & Mobile Gear", "High-Performance Auto", "Golf & Athletic Apparel", "Home Renovation & Fixtures", 
        "Luxury & Humidor Accessories", "Fine Arts & Creative Design", "Health & Wellness Tech", 
        "Beauty & Personal Care", "Eco-Friendly Living", "Smart Pet Tech", "Home Office Ergonomics", 
        "Outdoor & Survival Gear", "Gourmet Food & Culinary", "Men's Grooming", 
        "Travel Tech & Luggage", "Fitness & Recovery", "Gaming & Esports", 
        "Early Education Tech", "Smart Kitchen Gadgets"
    ]
    
    # Simulates live API pull routed through your new dynamic margin mapper
    for room in storefronts:
        for i in range(1, 26):
            raw_item = {
                "cost": random.uniform(8.00, 150.00), 
                "title": f"{room} Asset {i}",
                "category": room,
                "brand": "NEXUS Verified API",
                "sku": f"NX-{i}-{room[:3].upper()}"
            }
            inventory.append(map_supplier_data_to_nexus(raw_item))
            
    return inventory
