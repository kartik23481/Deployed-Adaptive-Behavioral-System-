# models/schema.py

from pydantic import BaseModel
from typing import Optional

# From backend -> frontend(GET requests)
class NewProduct(BaseModel):
    title: str
    price: str
    discount: str
    product_url: str
    image_link: str
    description: Optional[str]
    rating: str
    source: Optional[str]
    category: Optional[str]

# From frontend -> backend(POST requests)
class UserBehavior(BaseModel):
    query: str
    timeSpent: int
    scrollDepth: int
    clickCount: int
