from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

app = FastAPI(
    title="FastAPI Backstage Demo",
    description="API de ejemplo para integración con Backstage, ArgoCD, y Grafana",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: datetime = datetime.now()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# In-memory database para el ejemplo
items_db = [
    Item(id=1, name="Laptop", description="MacBook Pro", price=2500.0),
    Item(id=2, name="Mouse", description="Wireless mouse", price=25.0),
]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint para Kubernetes y monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "service": "fastapi-backstage-demo"
    }

# Metrics endpoint (para Prometheus)
@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint"""
    return {
        "total_items": len(items_db),
        "uptime": "healthy",
        "requests_total": "counter_value_here"
    }

# CRUD endpoints
@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint con información de la API"""
    return {
        "message": "FastAPI Backstage Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

@app.get("/items", response_model=List[Item], tags=["items"])
async def get_items():
    """Obtener todos los items"""
    return items_db

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def get_item(item_id: int):
    """Obtener un item por ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, tags=["items"])
async def create_item(item: ItemCreate):
    """Crear un nuevo item"""
    new_id = max([i.id for i in items_db], default=0) + 1
    new_item = Item(id=new_id, **item.dict())
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: int, item: ItemCreate):
    """Actualizar un item existente"""
    for i, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    """Eliminar un item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item {item_id} deleted", "deleted_item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)