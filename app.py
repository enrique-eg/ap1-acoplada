from flask import Flask, request, jsonify, render_template
from db import SessionLocal, init_db
from models import Item
import uuid

app = Flask(__name__)

# Inicializa la base de datos
with app.app_context():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create_item():
    data = request.get_json(force=True)
    item_id = str(uuid.uuid4())
    db = SessionLocal()
    try:
        item = Item(id=item_id, nombre=data.get("nombre"),
                    precio=float(data.get("precio")),
                    categoria=data.get("categoria"))
        db.add(item)
        db.commit()
        return jsonify({"id": item_id}), 201
    finally:
        db.close()

@app.get("/items")
def list_items():
    db = SessionLocal()
    try:
        items = db.query(Item).all()
        return jsonify([{
            "id": i.id,
            "nombre": i.nombre,
            "precio": i.precio,
            "categoria": i.categoria
        } for i in items])
    finally:
        db.close()

@app.get("/items/<item_id>")
def get_item(item_id):
    db = SessionLocal()
    try:
        item = db.get(Item, item_id)
        if not item:
            return jsonify({"message": "Not Found"}), 404
        return jsonify({
            "id": item.id,
            "nombre": item.nombre,
            "precio": item.precio,
            "categoria": item.categoria
        })
    finally:
        db.close()

@app.put("/items/<item_id>")
def update_item(item_id):
    data = request.get_json(force=True)
    db = SessionLocal()
    try:
        item = db.get(Item, item_id)
        if not item:
            return jsonify({"message": "Not Found"}), 404
        if "nombre" in data: item.nombre = data["nombre"]
        if "precio" in data: item.precio = float(data["precio"])
        if "categoria" in data: item.categoria = data["categoria"]
        db.commit()
        return jsonify({"message": "Updated"})
    finally:
        db.close()

@app.delete("/items/<item_id>")
def delete_item(item_id):
    db = SessionLocal()
    try:
        item = db.get(Item, item_id)
        if not item:
            return jsonify({"message": "Not Found"}), 404
        db.delete(item)
        db.commit()
        return jsonify({"message": "Deleted"})
    finally:
        db.close()

@app.get("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
