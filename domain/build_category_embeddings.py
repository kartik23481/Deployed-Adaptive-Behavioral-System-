import json
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

from categories import dict1,description

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "database")

all_categories = []

for category_group in dict1.values():
    all_categories.extend(category_group)


all_categories = list(set(all_categories))

def find_category_json(category_name):

    possible_paths = [

        # Evergreen
        os.path.join(DATABASE_DIR,"evergreen_categories",f"{category_name}.json"),

        # Summer
        os.path.join(DATABASE_DIR,"summer_categories",f"{category_name}.json"),

        # Rainy
        os.path.join(DATABASE_DIR,"rainy_categories",f"{category_name}.json"),

        # Winter
        os.path.join(DATABASE_DIR,"winter_categories",f"{category_name}.json")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

# Build category embeddings data

category_embeddings_data = {}

for category in all_categories:

    print(f"Processing: {category}")
    print(f"Description: {description[category]}")
    embedding = model.encode(description[category]).tolist()

    # Find representative image

    image_url = ""
    category_json_path = find_category_json(category)
    if category_json_path:
        try:
            with open(category_json_path, "r", encoding="utf-8") as f:
                products = json.load(f)
            if len(products) > 0:
                first_product = products[0]
                image_url = first_product.get("image_link","")

        except Exception as e:

            print(f"Error reading {category}: {e}")


    # Save category metadata

    category_embeddings_data[category] = {
        "embedding": embedding,
        "image_url": image_url,
        "category": category
    }

output_path = os.path.join(os.path.dirname(__file__),"category_embeddings.json")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("{\n")
    total = len(category_embeddings_data)
    for idx, (category, data) in enumerate(category_embeddings_data.items()):
        embedding_str = json.dumps(data["embedding"])
        entry = f'''  "{category}": {{
    "category": "{data["category"]}",
    "image_url": "{data["image_url"]}",
    "embedding": {embedding_str}
  }}'''

        if idx < total - 1:
            entry += ","

        entry += "\n"

        f.write(entry)

    f.write("}")

print("\nCategory embeddings JSON created successfully.")
print(f"Saved at: {output_path}")
print(f"Total categories: {len(category_embeddings_data)}")