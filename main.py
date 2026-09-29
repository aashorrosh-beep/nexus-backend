import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The live memory of the Matrix rooms. We start with your secure fallbacks.
live_inventory = [
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
        "sku": "NX-TCG-001",
        "name": "Pokemon 30th Celebration Ultra-Premium Collection",
        "price": 549.95,
        "stock_count": 8,
        "hero_image": "https://images.pokemontcg.io/cel25/15_hires.png",
        "images": ["https://images.pokemontcg.io/cel25/15_hires.png"],
        "shippingText": "FREE Secure Vault Dispatch",
        "storefront": "Trading Cards Vault",
        "specs": {"manufacturer": "The Pokemon Company", "condition": "Factory Sealed"}
    }
]

# Door 1: The Next.js Storefront pulls data from here
@app.get("/api/matrix")
async def get_matrix():
    return live_inventory

# Door 2: The Dual-Brain AI pushes live assets here
@app.post("/api/products")
async def receive_ai_asset(request: Request):
    data = await request.json()
    product = data.get("product", {})
    
    # Strip out any '$' or commas from the AI's price so the frontend doesn't crash
    raw_price = str(product.get("price", "0")).replace('$', '').replace(',', '')
    try:
        clean_price = float(raw_price)
    except ValueError:
        clean_price = 0.0

    # Format the exact shape required by the Next.js Matrix UI
    new_asset = {
        "sku": f"NX-AI-00{len(live_inventory) + 1}",
        "name": product.get("name", "Classified Luxury Asset"),
        "price": clean_price,
        "stock_count": 1,
        "hero_image": product.get("image_url", ""),
        "images": [product.get("image_url", "")],
        "shippingText": "FREE Secure Vault Dispatch",
        "storefront": "Nexus Prime Exclusives",
        "specs": {"source": "Dual-Brain AI", "authentication": "Auditor Verified", "status": "LIVE"}
    }
    
    # Inject the AI asset directly to the top of the Matrix
    live_inventory.insert(0, new_asset)
    
    return {"status": "success", "message": "Asset officially published to the storefront."}
