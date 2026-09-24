# -----------------------------------------------------------------------------
# PROCUREMENT LOGIC
# -----------------------------------------------------------------------------
def fetch_raw_storefront_assets(room_name: str) -> List[dict]:
    room_upper = room_name.upper()
    items = []

    if "PRE-RELEASE" in room_upper or "ROOM 21" in room_upper or "VAULT" in room_upper:
        allocations = [
            ("Tom Brady 1-of-1 Refractor Autograph", 3500.0, "Panini", 1, "12 x 8 x 2 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Tom+Brady+1-of-1"),
            ("Pokémon TCG: Booster Box Display", 550.0, "Pokémon", 12, "8 x 6 x 5 in", "3.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pokemon+Booster+Box"),
            ("One Piece TCG: Wings of Captain", 480.0, "Bandai", 8, "8 x 6 x 5 in", "3.0 lbs", "https://placehold.co/800x800/111/fcba03?text=One+Piece+Box"),
            ("Magic: The Gathering Collector Case", 1450.0, "Wizards", 4, "14 x 10 x 8 in", "8.5 lbs", "https://placehold.co/800x800/111/fcba03?text=MTG+Collector+Case"),
            ("Caitlin Clark Rookie Gold Refractor", 850.0, "Bowman", 2, "6 x 4 x 1 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Caitlin+Clark+Rookie"),
            ("Jordan Groshans 1st Bowman Auto", 250.0, "Topps", 5, "6 x 4 x 1 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Jordan+Groshans+Auto"),
            ("Tiger Woods 22KT Gold Collection", 1200.0, "Upper Deck", 2, "10 x 8 x 3 in", "2.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Tiger+Woods+Gold"),
            ("Pokémon TCG: Sealed Mini Tin 10-Pack", 320.0, "Pokémon", 15, "12 x 6 x 4 in", "4.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Pokemon+Mini+Tins"),
            ("NFL National Treasures Hobby Box", 2800.0, "Panini", 3, "10 x 10 x 6 in", "5.5 lbs", "https://placehold.co/800x800/111/fcba03?text=NFL+National+Treasures"),
            ("NBA Flawless Sealed Case", 4200.0, "Panini", 1, "16 x 12 x 10 in", "12.0 lbs", "https://placehold.co/800x800/111/fcba03?text=NBA+Flawless"),
            ("One Piece TCG: Awakening Case", 2200.0, "Bandai", 2, "14 x 10 x 8 in", "9.0 lbs", "https://placehold.co/800x800/111/fcba03?text=One+Piece+Awakening"),
            ("F1 Chrome Hobby Box Factory Sealed", 650.0, "Topps", 6, "9 x 6 x 4 in", "2.8 lbs", "https://placehold.co/800x800/111/fcba03?text=F1+Chrome+Box"),
            ("Shohei Ohtani Dual Auto Relic", 3100.0, "Topps", 1, "8 x 6 x 2 in", "1.8 lbs", "https://placehold.co/800x800/111/fcba03?text=Shohei+Ohtani+Auto"),
        ]
        for name, cost, brand, stock, dims, wt, img in allocations[:13]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified allocation asset. Vault-secured provenance for {name}.",
                "images": [img], "dimensions": dims, "weight": wt, "is_presale": True
            })
        return items
        
    elif "ROOM 22" in room_upper or "SQUISHMALLOW" in room_upper:
        # Expanded to 25 Items. Includes $8-$11 wholesale to hit $20-$25 retail pricing.
        allocations = [
            ("Squishmallows 8-Inch Mystery Squad Box", 9.0, "Kellytoy", 24, "8 x 8 x 8 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=8-Inch+Mystery+Squishmallow"),
            ("Pop Mart Skullpanda Everyday Wonderland Blind Box", 11.0, "Pop Mart", 15, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Skullpanda"),
            ("Jellycat Amuseable Boiled Egg (Small)", 10.0, "Jellycat", 18, "5 x 3 x 3 in", "0.3 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Egg"),
            ("Squishmallows 16-Inch Rare Connor The Cow", 45.0, "Kellytoy", 8, "16 x 16 x 16 in", "2.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Connor+The+Cow"),
            ("Sonny Angel Mini Figure Original Series (Single)", 9.5, "Dreams Inc.", 36, "3 x 2 x 2 in", "0.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Sonny+Angel+Single"),
            ("Smiski Glow-In-The-Dark Figure (Single)", 8.5, "Dreams Inc.", 40, "3 x 2 x 2 in", "0.1 lbs", "https://placehold.co/800x800/111/fcba03?text=Smiski+Glow+Figure"),
            ("Squishmallows 12-Inch Archie The Axolotl", 35.0, "Kellytoy", 14, "12 x 12 x 12 in", "1.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Archie+Axolotl"),
            ("Tokidoki Unicorno Series 12 Blind Box", 10.5, "Tokidoki", 27, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Tokidoki+Unicorno"),
            ("Jellycat Bashful Bunny (Medium)", 14.0, "Jellycat", 15, "12 x 5 x 4 in", "0.6 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Bunny"),
            ("Pop Mart Hirono City of Mercy Series (Single)", 12.0, "Pop Mart", 20, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Hirono"),
            ("Squishmallows 5-Inch Mini 6-Pack Assortment", 22.0, "Kellytoy", 10, "10 x 8 x 5 in", "1.0 lbs", "https://placehold.co/800x800/111/fcba03?text=5-Inch+Squishmallow+Pack"),
            ("Gudetama Lazy Egg Vinyl Figure Box", 11.0, "Sanrio", 12, "4 x 4 x 4 in", "0.3 lbs", "https://placehold.co/800x800/111/fcba03?text=Gudetama+Vinyl"),
            ("Squishmallows 14-Inch Gengar Pokemon Edition", 55.0, "Kellytoy", 9, "14 x 14 x 14 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Gengar+Squishmallow"),
            ("Pop Mart Dimoo Dating Series (Single)", 12.0, "Pop Mart", 18, "4 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pop+Mart+Dimoo"),
            ("Jellycat Amuseable Silly Succulent Plush", 32.0, "Jellycat", 18, "6 x 3 x 3 in", "0.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Succulent"),
            ("Pusheen Surprise Plush Series 18", 10.0, "Gund", 22, "3 x 3 x 3 in", "0.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Pusheen+Surprise"),
            ("Squishmallows Pokemon Pikachu 20-Inch Jumbo", 85.0, "Kellytoy", 4, "20 x 20 x 20 in", "3.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Pikachu+Jumbo"),
            ("Pop Mart Skullpanda Everyday Wonderland (Whole Set)", 145.0, "Pop Mart", 5, "12 x 8 x 6 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Skullpanda+Full+Set"),
            ("Sonny Angel Mini Figure Original Series (Case of 12)", 120.0, "Dreams Inc.", 6, "10 x 8 x 5 in", "1.8 lbs", "https://placehold.co/800x800/111/fcba03?text=Sonny+Angel+Case"),
            ("Smiski Glow-In-The-Dark Figure (Set of 6)", 65.0, "Dreams Inc.", 10, "8 x 6 x 4 in", "1.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Smiski+Set"),
            ("Jellycat Bashful Bunny Huge Size", 65.0, "Jellycat", 5, "20 x 8 x 6 in", "1.2 lbs", "https://placehold.co/800x800/111/fcba03?text=Jellycat+Huge"),
            ("Pop Mart Hirono City of Mercy Series (Whole Set)", 150.0, "Pop Mart", 3, "12 x 8 x 6 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Hirono+Full+Set"),
            ("Tokidoki Unicorno Series 12 Display Case", 110.0, "Tokidoki", 7, "10 x 8 x 6 in", "1.6 lbs", "https://placehold.co/800x800/111/fcba03?text=Tokidoki+Display"),
            ("Pop Mart Dimoo Dating Series (Whole Set)", 140.0, "Pop Mart", 4, "12 x 8 x 6 in", "1.5 lbs", "https://placehold.co/800x800/111/fcba03?text=Dimoo+Full+Set"),
            ("Squishmallows Jack the Black Cat (Limited Edition)", 250.0, "Kellytoy", 1, "16 x 16 x 16 in", "2.0 lbs", "https://placehold.co/800x800/111/fcba03?text=Jack+The+Black+Cat"),
        ]
        for name, cost, brand, stock, dims, wt, img in allocations[:25]:
            items.append({
                "title": name, "wholesale_cost": cost, "brand": brand, "stock": stock,
                "description": f"Verified authentic {brand} highly-allocated collectible. Mint condition.",
                "images": [img], "dimensions": dims, "weight": wt, "is_presale": False
            })
        return items

    query_map = {
        "TECH": "smart gadgets", "AUTO": "automotive parts", "GOLF": "golf accessories",
        "HOME": "luxury home fixtures", "HUMIDOR": "cigar humidor", "ART": "sculpture design",
        "WELLNESS": "recovery tech", "BEAUTY": "skincare tools", "ECO": "sustainable living",
        "PET": "smart pet", "OFFICE": "ergonomic office", "OUTDOOR": "tactical survival"
    }
    
    search_q = "premium"
    for key, val in query_map.items():
        if key in room_upper: search_q = val; break

    try:
        url = f"https://dummyjson.com/products/search?q={urllib.parse.quote(search_q)}&limit=13"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as res:
            data = json.loads(res.read().decode())
            for p in data.get("products", []):
                items.append({
                    "title": p.get("title"), "wholesale_cost": float(p.get("price", 50.0)),
                    "brand": p.get("brand", "Verified Manufacturer"), "stock": p.get("stock", random.randint(15, 60)),
                    "description": p.get("description"), "images": p.get("images", []),
                    "dimensions": "14 x 10 x 6 in", "weight": f"{round(random.uniform(1.5, 6.0), 1)} lbs",
                    "is_presale": False
                })
    except Exception:
        pass

    idx = 1
    # Expand default commodity rooms to 13 items
    while len(items) < 13:
        items.append({
            "title": f"{room_name} Premium Asset {idx:02d}", "wholesale_cost": round(random.uniform(45.0, 220.0), 2),
            "brand": "Direct Manufacturer Verified", "stock": random.randint(20, 80),
            "description": f"Engineered architectural grade specification for {room_name}.",
            "images": [], "dimensions": "18 x 12 x 8 in", "weight": "4.2 lbs", "is_presale": False
        })
        idx += 1

    return items
