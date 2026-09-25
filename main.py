@app.get("/api/matrix")
async def get_matrix():
    if not ZENDROP_KEY:
        return [{"sku": "ERROR", "name": "API KEY MISSING", "price": 0.0, "stock_count": 0, "hero_image": "https://via.placeholder.com/800", "images": [], "shippingText": "ERROR", "storefront": "System Diagnostics", "specs": {}}]

    try:
        headers = {"Authorization": f"Bearer {ZENDROP_KEY}", "Content-Type": "application/json"}
        response = requests.get("https://api.zendrop.com/v1/products", headers=headers, timeout=15)
        
        # This will catch whatever raw text Zendrop is returning, even if it's an HTML error
        try:
            live_items = response.json().get('data', [])
        except Exception:
            return [{
                "sku": "ERROR-FORMAT", 
                "name": f"ZENDROP SENT JUNK DATA: {response.text[:150]}", 
                "price": 0.00,
                "stock_count": 0, 
                "hero_image": "https://via.placeholder.com/800?text=ZENDROP+FORMAT+ERROR",
                "images": [], "shippingText": "ERROR", "storefront": "System Diagnostics", "specs": {}
            }]

        inventory = []
        for raw_item in live_items:
            images = raw_item.get('images', [])
            if not images or len(images) == 0:
                continue
            if int(raw_item.get('inventory_quantity', 0)) <= 0:
                continue
            inventory.append(map_supplier_data_to_nexus(raw_item))
            
        return inventory
        
    except Exception as e:
        return [{"sku": "ERROR-CRASH", "name": f"Backend Crash: {str(e)}", "price": 0.0, "stock_count": 0, "hero_image": "https://via.placeholder.com/800", "images": [], "shippingText": "ERROR", "storefront": "System Diagnostics", "specs": {}}]
