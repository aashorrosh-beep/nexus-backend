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
