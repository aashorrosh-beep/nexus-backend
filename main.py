from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="ALBS Back-of-House Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ALBS HIGH-FIDELITY CURATED VAULT (13 ROOMS)
ROOM_ASSETS = {
    "sneaker_footwear_vault": {"cap": 6, "img": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?q=80&w=500", "items": ["Velocity Pro High-Top", "Stealth Runner V2", "Phantom Court Classic", "Aero Glide Trainer", "Neon Retro Kicks", "Urban Shadow Edition"]},
    "apparel_streetwear_hub": {"cap": 5, "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?q=80&w=500", "items": ["Zero-G Shell Jacket", "Heavyweight Box Hoodie", "Tactical Cargo Jogger", "Thermal Base Layer", "Oversized Utility Tee"]},
    "toys_games_novelties": {"cap": 6, "img": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?q=80&w=500", "items": ["Magnetic Levitation Globe", "Retro Arcade Console", "Drone Racing Kit", "Holographic Chess Set", "Smart Puzzle Cube", "Neon LED Sign"]},
    "tech_mobile_gear": {"cap": 5, "img": "https://images.unsplash.com/photo-1585338107529-13afc5f02586?q=80&w=500", "items": ["Magnetic Wireless Array", "Noise-Canceling Pods", "Graphite Power Bank", "Titanium Smart Band", "AR Commuter Glasses"]},
    "beauty_self_care_lab": {"cap": 7, "img": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?q=80&w=500", "items": ["Sonic Facial Sculptor", "Organic Vitamin C Serum", "LED Therapy Mask", "Hydration Sleep Matrix", "Rose Quartz Roller", "Peptide Eye Cream", "Botanical Hair Elixir"]},
    "health_wellness_bar": {"cap": 6, "img": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?q=80&w=500", "items": ["Smart Posture Corrector", "Deep Tissue Massage Gun", "Acupressure Relief Mat", "Cold Plunge Tub", "Infrared Sauna Blanket", "Sleep Tracking Ring"]},
    "home_lifestyle_living": {"cap": 5, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?q=80&w=500", "items": ["Smart Ambient Projector", "Ceramic Diffuser Hub", "Minimalist Desk Lamp", "Gravity Blanket", "Hydroponic Garden Planter"]},
    "fitness_recovery_core": {"cap": 6, "img": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?q=80&w=500", "items": ["Adjustable Dumbbell Set", "Smart Jump Rope", "Vibrating Foam Roller", "Resistance Band Array", "Core Slider Plates", "Cryotherapy Knee Wrap"]},
    "pet_lifestyle_bar": {"cap": 5, "img": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=500", "items": ["Automatic Smart Feeder", "Orthopedic Memory Bed", "GPS Tracking Collar", "Self-Cleaning Litter Bot", "Interactive Laser Toy"]},
    "kitchen_smart_gadgets": {"cap": 7, "img": "https://images.unsplash.com/photo-1556910103-1c02745a872f?q=80&w=500", "items": ["Digital Air Fryer Pro", "Smart Temperature Mug", "Precision Sous Vide", "Automatic Espresso Bar", "Cold Brew Generator", "Touchless Soap Dispenser", "Magnetic Spice Rack"]},
    "travel_edc_essentials": {"cap": 5, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=500", "items": ["Hard-Shell Carry-On", "Anti-Theft Commuter Bag", "Universal Power Adapter", "Compressible Packing Cubes", "Titanium Pocket Tool"]},
    "curated_mystery_boxes": {"cap": 6, "img": "https://images.unsplash.com/photo-1608298934526-7e44a4714db0?q=80&w=500", "items": ["Tech Hype Box", "Streetwear Premium Crate", "Sneakerhead Grail Box", "Gamer Ultimate Drop", "Fitness Starter Kit", "EDC Surprise Vault"]},
    "trading_cards_vault": {"cap": 6, "img": "https://images.unsplash.com/photo-1613336026275-d6d473084e85?q=80&w=500", "items": ["TCG Elite Trainer Box", "Magic Booster Display Box", "Sealed Mini Tin Collection", "Premium Toploader Bundle", "Graded Card Display Case", "Vintage Mystery Pack"]}
}

def generate_beautiful_inventory():
    vaults = {}
    for room, data in ROOM_ASSETS.items():
        room_inventory = []
        for i in range(data["cap"]):
            score = round(random.uniform(20.0, 60.0), 2)
            tag = "VIRAL ALERT" if score > 50 else "TRENDING" if score > 35 else "SELLING FAST"
            
            room_inventory.append({
                "id": f"{room[:3]}_{i}",
                "name": data["items"][i],
                "price": round(random.uniform(49.99, 299.99), 2),
                "stock": "Low",
                "tag": tag,
                "image": data["img"]
            })
        vaults[room] = sorted(room_inventory, key=lambda x: x["price"], reverse=True)
    return vaults

MASTER_INVENTORY = generate_beautiful_inventory()

@app.get("/api/storefront/{category}")
async def get_category_drop(category: str):
    category_key = category.lower().replace("-", "_").replace(" ", "_")
    if category_key not in MASTER_INVENTORY:
        raise HTTPException(status_code=404, detail="Storefront not found.")
    return {
        "status": "LIVE",
        "category": category.upper(),
        "items": MASTER_INVENTORY[category_key]
    }
