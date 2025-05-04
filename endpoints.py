from fastapi import FastAPI
from chome.quickstart import oath

app = FastAPI()
oauth_instance = oath()

@app.get("/locations", description="Fetch raw Kroger locations by ZIP code")
def locations(zipCode: str = "97124", limit: int = 13):
    return oauth_instance.get_loct(zipCode, limit)

@app.get("/products", description="Fetch structured Kroger products by locationId and search term")
def products(locationId: int = 70100661, search: str = "coffee", results: int = 44):
    return oauth_instance.structure_pos(locationId, search, results)

@app.get("/product-aisle", description="Fetch aisleLocations by productId and")
def product_aisle(productId: str, locationId: int = 70100661):
    return oauth_instance.get_aisle_info_by_id(productId, locationId)
