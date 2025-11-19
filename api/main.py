from fastapi import FastAPI, WebSocket
import random
import asyncio
import uvicorn
import json

app = FastAPI(title="DataCo Streaming (aligned with Spark model)")

# -----------------------------
# 1) VALEURS POSSIBLES
# -----------------------------
TYPES = ["DEBIT", "TRANSFER", "CASH", "PAYMENT"]
SHIPPING = ["Standard Class", "First Class", "Second Class", "Same Day"]
MARKETS = ["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
REGIONS = [
    "East of USA", "West of USA", "Southern Europe", "Northern Europe",
    "Central Asia", "South America", "Canada", "East Africa", "West Africa", "Southeast Asia"
]
CATEGORIES = ["Furniture", "Technology", "Office Supplies", "Binders", "Art", "Sporting Goods"]

# -----------------------------
# 2) Génération d’un enregistrement (exactement tes colonnes)
# -----------------------------
def generate_record():

    shipping_mode = random.choice(SHIPPING)

    # Jours de livraison réalistes
    if shipping_mode == "Same Day":
        days = 0
    elif shipping_mode in ["First Class", "Second Class"]:
        days = random.choice([1, 2])
    else:
        days = 4

    # Données réalistes inspirées de ton Streamlit
    sales = round(random.uniform(100, 500), 2)
    discount = round(random.uniform(0, 50), 2)
    price = round(random.uniform(200, 400), 2)
    quantity = random.choice([1, 2, 3, 4])

    benefit = round(random.uniform(-20, 150), 2)
    profit_ratio = round(benefit / price, 2) if price != 0 else 0
    discount_rate = round(discount / price, 3) if price != 0 else 0

    # ⚠️ Tes colonnes EXACTES
    return {
        "Days for shipment (scheduled)": days,
        "Benefit per order": benefit,
        "Sales per customer": round(sales * random.uniform(0.8, 1.2), 2),
        "Order Item Discount": discount,
        "Order Item Discount Rate": discount_rate,
        "Order Item Product Price": price,
        "Order Item Profit Ratio": profit_ratio,
        "Order Item Quantity": quantity,
        "Sales": sales,
        "Order Profit Per Order": benefit,

        "Type": random.choice(TYPES),
        "Shipping Mode": shipping_mode,
        "Market": random.choice(MARKETS),
        "Customer Segment": random.choice(SEGMENTS),
        "Order Region": random.choice(REGIONS),
        "Category Name": random.choice(CATEGORIES)
    }

# -----------------------------
# 3) Accueil
# -----------------------------
@app.get("/")
async def root():
    return {"status": "API online", "websocket": "/ws"}

# -----------------------------
# 4) WebSocket (streaming)
# -----------------------------
@app.websocket("/ws")
async def stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connecté")

    try:
        while True:
            record = generate_record()
            await websocket.send_text(json.dumps(record))
            print("Envoyé :", record)

            await asyncio.sleep(2)

    except Exception as e:
        print("Déconnexion :", e)
    finally:
        await websocket.close()

# -----------------------------
# 5) Lancer l’API
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
