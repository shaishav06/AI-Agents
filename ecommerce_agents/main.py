from fastapi import FastAPI
from agents.inventory_agent import InventoryAgent

app = FastAPI()

@app.get("/inventory/{product_id}")
def check_inventory(product_id: str):
    agent = InventoryAgent()
    return {"message": agent.check_stock(product_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
