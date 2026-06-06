
dict1 = {
    "evergreen_categories": ["mobiles", "laptops", "headphones", "smartwatches", "bedsheets","casual_shoes","chargers_cables","earbuds","face_wash" ,"jeans" , "kitchen_appliances" ,"powerbanks","trimmers","smart_tvs","office_bags","backpacks"],
    "summer_categories": ["air_conditioners", "baby_clothes", "sunglasses", "cooler_bags" , "cotton_curtains", "cotton_kurtas","face_mist" , "flip_flops" , "mini_fans" , "moisturizers" ,"shorts" , "sunscreen",  "tshirts"  ,"usb_fans" , "water_bottles"],
    "rainy_categories": ["raincoats", "umbrellas", "waterproof_backpacks", "waterproof_shoes"],
    "winter_categories": ["blankets", "hoodies", "jackets", "room_heaters", "sweaters", "winter_skin_care"]
}

# -- Dict 2: Synonym mapping

dict2 = {
    "raincoats": ["raincoat","raincoats"],
    "umbrellas": ["umbrella","umbrellas"],
    "waterproof_shoes": ["waterproof shoes","waterproofshoe","waterproofshoes"],
    "waterproof_backpacks": ["waterproof backpacks","waterproofbackpacks","waterproof backpack"],
    "jackets": ["jacket","jackets"],
    "hoodies": ["hoodie","hoodies"],
    "sweaters": ["sweater","sweaters"],
    "blankets": ["blanket","blankets"],
    "room_heaters": ["room heater","room heaters"],
    "winter_skin_care": ["winter skin care","winterskincare","winter skincare"],
    "trimmers": ["trimmer","trimmers"],
    "smart_tvs": ["tvs","tv","televisions","smart tv","smart tvs","smarttv","smarttvs"],
    "office_bags": ["office bags","officebag","officebags"],
    "backpacks": ["backpack","backpacks"],
    "usb_fans":["usb fans","usbfans"],
    "tshirts": ["tshirt","tshirts"],
    "sunscreen": ["sunscreen","sunscreens","sun screen"],
    "shorts": ["shorts","short"],
    "moisturizers": ["moisturizers","moisturizer"],
    "mini_fans": ["mini fans","minifans"],
    "flip_flops": ["flipflop","flipflops","flip flops"],
    "face_mist": ["facemist","face mist"],
    "cotton_kurtas": ["kurtas","curtas","cotton kurtas","curta","kurta"],
    "cotton_curtains": ["curtains","cotton curtains","cottoncurtains"],
    "cooler_bags": ["cooler_bags","coolerbag","coolerbags","cooler bags"],
    "sunglasses": ["sunglass","sunglasses"],
    "water_bottles": ["waterbottles","water bottles","waterbottle","water bottle"],
    "baby_clothes": ["baby clothes","babyclothes"],
    "air_conditioners": ["airconditioners","air conditioners","air_conditioners","aircooler","cooler","ac"],
    "powerbanks": ["powerbank","powerbanks"],
    "kitchen_appliances": ["kitchen","kitchen appliances","kitchen items"],
    "jeans": ["jeans","jean","pants","pant"],
    "face_wash": ["facewash","face wash"],
    "earbuds": ["earbud","earbuds"],
    "Chargers & Cables": ["charger","chargers","cables","cable"],
    "casual_shoes" : ["shoes","casual shoes","casualshoes"],
    "headphones" : ["headphones","headphone"],
    "mobiles": ["mobile", "mobiles", "phone", "phones"],
    "laptops": ["laptop", "laptops"],
    "smartwatches": ["smartwatch", "smartwatches"],
    "bedsheets": ["bedsheet", "bedsheets"]
}

# selector value and selector class for each category

seasonal_categories = {
    "evergreen_categories" : {
        "mobiles": {"url": "https://www.flipkart.com/search?q=mobiles","selector_type": "class","selector_value": "jIjQ8S"},
        "laptops": {"url": "https://www.flipkart.com/search?q=laptops","selector_type": "class","selector_value": "jIjQ8S"},
        "earbuds": {"url": "https://www.flipkart.com/search?q=earbuds","selector_type": "class","selector_value": "RGLWAk"},
        "smartwatches": {"url": "https://www.flipkart.com/search?q=smartwatches","selector_type": "data-id","selector_value": "SMW"},
        "jeans": {"url": "https://www.flipkart.com/search?q=jeans","selector_type": "data-id","selector_value": "JEA"},
        "casual_shoes": {"url": "https://www.flipkart.com/search?q=casual+shoes","selector_type": "data-id","selector_value": "SHO"},
        "kitchen_appliances": {"url": "https://www.flipkart.com/search?q=kitchen+appliances","selector_type": "class","selector_value": "RGLWAk"},
        "face_wash": {"url": "https://www.flipkart.com/search?q=face+wash","selector_type": "class","selector_value": "RGLWAk"},
        "bedsheets": {"url": "https://www.flipkart.com/search?q=bedsheets","selector_type": "class","selector_value": "RGLWAk"},
        "headphones": {"url": "https://www.flipkart.com/search?q=headphones","selector_type": "class","selector_value": "RGLWAk"},
        "powerbanks": {"url": "https://www.flipkart.com/search?q=powerbanks","selector_type": "class","selector_value": "RGLWAk"},
        "Chargers & Cables": {"url": "https://www.flipkart.com/search?q=Chargers&Cables","selector_type": "class","selector_value": "RGLWAk"},
        "trimmers": {"url": "https://www.flipkart.com/search?q=trimmers","selector_type": "class","selector_value": "RGLWAk"},
        "backpacks": {"url": "https://www.flipkart.com/search?q=backpacks","selector_type": "data-id","selector_value": "BKP"},
        "office_bags": {"url": "https://www.flipkart.com/search?q=office+bags","selector_type": "data-id","selector_value": "BKP"},
        "smart_tvs": {"url": "https://www.flipkart.com/search?q=smart+tv","selector_type": "class","selector_value": "jIjQ8S"}
    },
    "summer_categories":{
        "tshirts": {"url": "https://www.flipkart.com/search?q=tshirts", "selector_type": "data-id", "selector_value": "TSH"},
        "shorts": {"url": "https://www.flipkart.com/search?q=shorts+men+women", "selector_type": "data-id", "selector_value": "SRT"},
        "cotton_kurtas": {"url": "https://www.flipkart.com/search?q=cotton+kurtas", "selector_type": "data-id", "selector_value": "KTA"},
        "cooler_bags": {"url": "https://www.flipkart.com/search?q=cooler+bags", "selector_type": "class", "selector_value": "RGLWAk"},
        "sunglasses": {"url": "https://www.flipkart.com/search?q=sunglasses", "selector_type": "data-id", "selector_value": "SGL"},
        "flip_flops": {"url": "https://www.flipkart.com/search?q=flip+flops", "selector_type": "data-id", "selector_value": "SFF"},
        "air_conditioners": {"url": "https://www.flipkart.com/search?q=air+conditioners", "selector_type": "class", "selector_value": "jIjQ8S"},
        "air_coolers": {"url": "https://www.flipkart.com/search?q=air+coolers", "selector_type": "class", "selector_value": "RGLWAk"},
        "usb_fans": {"url": "https://www.flipkart.com/search?q=mini+usb+fans", "selector_type": "class", "selector_value": "RGLWAk"},
        "sunscreen": {"url": "https://www.flipkart.com/search?q=sunscreen", "selector_type": "class", "selector_value": "RGLWAk"},
        "face_mist": {"url": "https://www.flipkart.com/search?q=face+mist", "selector_type": "class", "selector_value": "RGLWAk"},
        "moisturizers": {"url": "https://www.flipkart.com/search?q=non+greasy+moisturizer", "selector_type": "class", "selector_value": "RGLWAk"},
        "cooling_bedsheets": {"url": "https://www.flipkart.com/search?q=cooling+bedsheets", "selector_type": "class", "selector_value": "RGLWAk"},
        "cotton_curtains": {"url": "https://www.flipkart.com/search?q=cotton+curtains", "selector_type": "class", "selector_value": "RGLWAk"},
        "water_bottles": {"url": "https://www.flipkart.com/search?q=insulated+water+bottle", "selector_type": "class", "selector_value": "RGLWAk"},
        "baby_clothes": {"url": "https://www.flipkart.com/search?q=summer+baby+clothes", "selector_type": "data-id", "selector_value": "KPB"},
        "mini_fans": {"url": "https://www.flipkart.com/search?q=portable+mini+fans", "selector_type": "class", "selector_value": "RGLWAk"}
    },
    "winter_categories": {
        "jackets": {"url": "https://www.flipkart.com/search?q=jackets", "selector_type": "data-id", "selector_value": "JCK"},
        "hoodies": {"url": "https://www.flipkart.com/search?q=hoodies", "selector_type": "data-id", "selector_value": "SWS"},
        "sweaters": {"url": "https://www.flipkart.com/search?q=sweaters", "selector_type": "data-id", "selector_value": "SWT"},
        "blankets": {"url": "https://www.flipkart.com/search?q=blankets", "selector_type": "class", "selector_value": "RGLWAk"},
        "room_heaters": {"url": "https://www.flipkart.com/search?q=room+heater", "selector_type": "class", "selector_value": "RGLWAk"},
        "winter_skin_care": {"url": "https://www.flipkart.com/search?q=winter+skin+care", "selector_type": "class", "selector_value": "RGLWAk"}
    },
    "rainy_categories": {
        "umbrellas":{"url":"https://www.flipkart.com/search?q=umbrellas","selector_type":"class","selector_value":"RGLWAk"},
        "raincoats":{"url":"https://www.flipkart.com/search?q=raincoats","selector_type":"data-id","selector_value":"RNC"},
        "waterproof_shoes":{"url":"https://www.flipkart.com/search?q=waterproof+shoes","selector_type":"data-id","selector_value":"SHO"},
        "waterproof_backpacks":{"url":"https://www.flipkart.com/search?q=waterproof+backpacks","selector_type":"data-id","selector_value":"BKP"}
    }
}

description = {
  "mobiles": "Smartphones and mobile phones for daily communication, featuring touchscreens, high-resolution cameras, and app ecosystems. Distinct from tablets or laptops by their compact handheld form, cellular SIM connectivity, and pocket-sized portability. Used for calling, messaging, photography, social media, and mobile internet browsing throughout the day.",

  "laptops": "Portable personal computers with a physical keyboard, hinged screen, and built-in battery for computing on the go. Used for work, programming, content creation, and studying — distinct from tablets by their full keyboard and desktop-grade processing power. Suitable for office, home, and travel use.",

  "headphones": "Over-ear and on-ear audio devices worn on the head for immersive private listening. Feature cushioned ear cups, adjustable headband, and wired or wireless Bluetooth connectivity. Distinct from earbuds by their larger drivers, superior sound isolation, and extended wearing comfort for music, gaming, and calls.",

  "smartwatches": "Wrist-worn smart devices that display notifications, track fitness metrics like steps and heart rate, and sync with smartphones. Distinct from traditional watches by their digital touchscreen interface, health sensors, and app support. Used for fitness monitoring, quick glances at alerts, and contactless payments.",

  "bedsheets": "Flat and fitted fabric sheets designed to cover a mattress and provide a comfortable sleeping surface. Made from cotton, microfiber, or linen in single, double, and king sizes. Distinct from blankets or duvets by their thin flat form and direct mattress contact. Used in bedrooms for daily sleeping comfort.",

  "casual_shoes": "Everyday lace-up and slip-on shoes designed for comfort during walking, commuting, and informal outings. Made from canvas, leather, or synthetic materials with cushioned soles. Distinct from sports shoes by their lifestyle-oriented design and from formal shoes by their relaxed non-dressy appearance.",

  "chargers_cables": "Wired charging accessories including USB-C, micro-USB, and Lightning cables along with wall adapters and fast chargers for powering smartphones, tablets, and laptops. Distinct from power banks by requiring a wall socket. Essential everyday accessories for keeping electronic devices charged at home and office.",

  "earbuds": "Compact in-ear wireless audio devices that sit inside the ear canal, offering portability and passive noise isolation. Feature Bluetooth connectivity, touch controls, and a compact charging case. Distinct from headphones by their miniature size, truly wireless design, and suitability for workouts and commuting.",

  "face_wash": "Gel, foam, or cream facial cleansers formulated to remove dirt, oil, and impurities from the face without stripping moisture. Used twice daily as part of a skincare routine. Distinct from body wash or soap by their gentle pH-balanced formula designed specifically for facial skin.",

  "jeans": "Durable denim trousers available in slim, straight, and relaxed fits for men and women. Characterized by riveted pockets, a sturdy waistband, and indigo or black denim fabric. Distinct from trousers or chinos by their casual denim construction. Worn for everyday outings, casual workplaces, and social settings.",

  "kitchen_appliances": "Electric cooking and food preparation devices for home kitchens including mixer grinders, microwaves, induction cooktops, toasters, and electric kettles. Distinct from cookware by their motorized or electrically powered operation. Used daily to speed up cooking, blending, heating, and food processing tasks in the kitchen.",

  "powerbanks": "Portable battery packs used to charge smartphones and small electronics on the go without access to a wall socket. Characterized by their rectangular form, USB output ports, and capacity measured in mAh. Distinct from wall chargers by their self-contained battery that enables charging anywhere.",

  "trimmers": "Electric grooming devices for trimming and shaping facial hair, beards, and body hair at home. Feature adjustable length combs, stainless steel blades, and cordless rechargeable operation. Distinct from razors by their ability to maintain stubble and beard length rather than achieving a clean shave.",

  "smart_tvs": "Large-screen internet-connected televisions with built-in streaming apps like Netflix and YouTube, voice control, and 4K or Full HD display. Distinct from monitors by their remote-operated TV interface and broadcast tuner. Used as the primary home entertainment screen for streaming, OTT content, and live television.",

  "office_bags": "Professional laptop bags, briefcases, and messenger bags designed to carry laptops, documents, and office accessories during daily commutes. Feature padded laptop compartments and organized pockets. Distinct from backpacks by their formal structured appearance and suitability for corporate and business environments.",

  "backpacks": "Two-strap bags worn on the back for carrying books, laptops, and daily essentials during college, travel, and casual outings. Feature multiple zippered compartments and padded shoulder straps. Distinct from office bags by their casual sporty design and from hiking bags by their everyday urban use.",

  "air_conditioners": "Fixed or portable cooling appliances that regulate indoor temperature during hot summer months by circulating refrigerated air. Available as split, window, and portable units measured in tonnage. Distinct from fans by their active cooling via refrigerant. Used primarily in bedrooms and living rooms during peak summer heat.",

  "baby_clothes": "Soft comfortable garments for infants and toddlers aged 0 to 3 years including onesies, rompers, and sleep suits. Made from gentle hypoallergenic cotton fabrics safe for sensitive baby skin. Distinct from children's clothing by their snap buttons, stretchable fabric, and age-specific tiny sizing.",

  "sunglasses": "UV-protective eyewear worn outdoors to shield eyes from bright sunlight and ultraviolet radiation. Available in polarized, mirrored, and tinted lenses with plastic or metal frames. Distinct from prescription glasses by their purely protective and fashion-oriented function. Used during summer outdoor activities, driving, and beach outings.",

  "cooler_bags": "Insulated portable bags and boxes designed to keep food, beverages, and perishables cold during outdoor trips, picnics, and travel. Feature thermal lining and sealed zippers. Distinct from regular bags by their heat-insulating inner layer. Used in summer for outdoor meals, road trips, and grocery transport.",

  "cotton_curtains": "Lightweight breathable window curtains made from cotton fabric for home decoration and sunlight filtering. Available in printed and solid colors for living rooms and bedrooms. Distinct from blackout curtains by their semi-sheer light-diffusing quality and from polyester curtains by their natural breathable cotton weave.",

  "cotton_kurtas": "Traditional Indian ethnic tops made from soft cotton fabric for men and women, featuring a straight or A-line silhouette with a center placket. Worn during casual outings, festivals, and summer days. Distinct from shirts by their ethnic design and longer hem length suited to Indian wear.",

  "face_mist": "Lightweight hydrating facial sprays used to refresh, cool, and moisturize skin throughout the day. Applied directly to the face from a fine-mist bottle. Distinct from toners by their on-the-go spray format and from moisturizers by their water-based cooling effect. Popular in summer for instant skin refreshment.",

  "flip_flops": "Lightweight open-toe flat sandals with a Y-shaped thong strap worn casually in summer. Made from rubber or foam soles for beach outings, poolside use, and quick errands. Distinct from sandals by their minimal thong-only strap and from shoes by their completely open backless design.",

  "mini_fans": "Small portable battery-operated or USB-powered personal fans for individual cooling during hot weather. Compact enough to fit on a desk or be held in hand. Distinct from ceiling or table fans by their personal miniature size and from air conditioners by their simple air circulation without cooling.",

  "moisturizers": "Hydrating face and body creams, lotions, and gels that restore and lock skin moisture after cleansing. Used daily in skincare routines for soft smooth skin. Distinct from face wash by their leave-on hydrating formula and from sunscreen by their primary focus on hydration rather than UV protection.",

  "shorts": "Short-length casual bottoms ending above the knee worn by men and women during summer. Made from cotton, denim, or jersey fabric for home wear, beach outings, and casual activities. Distinct from trousers and jeans by their above-knee length and from swimwear by their general casual land use.",

  "sunscreen": "Sun protection creams, lotions, and gels with SPF rating applied to exposed skin to block ultraviolet radiation and prevent tanning and sunburn. Used before outdoor exposure in summer. Distinct from moisturizers by their active UV-blocking chemical or mineral filters and their outdoor protective purpose.",

  "tshirts": "Casual short-sleeve tops with round or V-neck collar made from lightweight cotton or cotton-blend fabric for men and women. Worn during warm weather for everyday casual outings, home wear, and informal social settings. Distinct from shirts by their collarless design and from sweatshirts by their short sleeves and thin fabric.",

  "usb_fans": "Compact desk fans powered via USB connection to laptops, power banks, or USB adapters for personal cooling at workstations during summer. Distinct from battery fans by their continuous USB power source and from room fans by their small personal desk size. Used for office desk and study table cooling.",

  "water_bottles": "Reusable personal drinking bottles made from stainless steel, plastic, or glass for carrying water during outdoor activities, gym, office, and travel. Available in insulated and non-insulated variants. Distinct from cooler bags by their single-serving drinking form and from disposable bottles by their durable reusable construction.",

  "raincoats": "Waterproof full-length or knee-length outerwear garments worn over clothing to stay dry during heavy rainfall. Made from PVC, nylon, or polyester with sealed seams and a hood. Distinct from jackets by their primary waterproof rain protection function and from umbrellas by being worn on the body.",

  "umbrellas": "Handheld collapsible canopies with a telescopic or straight handle used to shield from rain and direct sunlight when outdoors. Distinct from raincoats by their handheld non-wearable form and from caps by their full overhead coverage. Used daily during monsoon season for walking and commuting in rain.",

  "waterproof_backpacks": "Rain-resistant and fully waterproof two-strap bags designed to protect laptops, books, and electronics during monsoon and wet weather commutes. Feature water-sealed zippers and coated fabric. Distinct from regular backpacks by their waterproof construction and from raincoats by being a bag rather than clothing.",

  "waterproof_shoes": "Closed-toe footwear with waterproof membranes or coated uppers designed to keep feet dry when walking in rain, puddles, and wet surfaces. Distinct from casual shoes by their sealed waterproof construction and from rain boots by their everyday wearable shoe form rather than tall rubber boot design.",

  "blankets": "Thick warm bed covers made from fleece, wool, or microfiber used during cold nights for insulation and warmth while sleeping or resting. Distinct from bedsheets by their heavy insulating thickness and from duvets by their single-layer construction without an inner filling. Used primarily in winter on beds and sofas.",

  "hoodies": "Full-sleeve sweatshirts with an attached hood and a front kangaroo pocket made from fleece or cotton-blend fabric for warmth in cool weather. Distinct from jackets by their soft sweatshirt construction without buttons or zippers in most styles and from sweaters by their hood and casual streetwear identity.",

  "jackets": "Structured outerwear garments with full-length zipper or button closure worn over clothing for warmth and protection in cold weather and outdoors. Made from denim, leather, polyester, or quilted fabric. Distinct from hoodies by their structured exterior shell and from sweaters by their outerwear layering purpose.",

  "room_heaters": "Electric appliances that generate and radiate heat to warm indoor rooms during cold winter months. Available as fan heaters, oil-filled radiators, and infrared heaters. Distinct from air conditioners by their heat-only function and from blankets by their ability to warm an entire room rather than an individual.",

  "sweaters": "Knitted full-sleeve pullovers and cardigans made from wool, acrylic, or cotton-blend yarn for warmth during cold and winter weather. Distinct from hoodies by their knitted fabric construction and absence of a hood and from jackets by their soft knitwear form without an outer shell.",

  "winter_skin_care": "Thick nourishing creams, body butters, lip balms, and intensive moisturizers formulated to combat dry cracked skin caused by cold dry winter air. Distinct from regular moisturizers by their heavier occlusive formula for extreme dryness and from face wash by their protective leave-on application during winter months."
}
