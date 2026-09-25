def map_supplier_data_to_nexus(raw_api_item):
    # 1. Pull the raw wholesale cost from the API payload
    wholesale_cost = float(raw_api_item.get('cost', 0.00))
    
    # 2. Run the dynamic economics engine to protect the 30% net margin
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

    # 3. Extract the high-fidelity media and specs (The Missing Link)
    # If the API doesn't have a video, it safely falls back to None so the frontend doesn't crash
    raw_images = raw_api_item.get('images', [])
    hero_img = raw_images[0] if len(raw_images) > 0 else "https://via.placeholder.com/800x800.png?text=IMAGE+SYNCING"
    
    return {
        "sku": raw_api_item.get('sku', f"DS-VERIFIED-{str(id(raw_api_item))[-6:]}"),
        "name": raw_api_item.get('title', 'Verified Manufacturer Asset'),
        "price": round(retail_price, 2),
        "stock_count": raw_api_item.get('inventory_quantity', 15),
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
