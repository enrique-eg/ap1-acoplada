from flask import Flask, request, jsonify, render_template
from db import create_item, get_item, list_items, update_item, delete_item

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create():
    data = request.get_json(force=True)
    item_id = create_item(data["nombre"], float(data["precio"]), data.get("categoria"))
    return jsonify({"id": item_id}), 201

@app.get("/items")
def list_all():
    return jsonify(list_items())

@app.get("/items/<item_id>")
def get_one(item_id):
    item = get_item(item_id)
    if not item:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(item)

@app.put("/items/<item_id>")
def update(item_id):
    data = request.get_json(force=True)
    update_item(item_id, data)
    return jsonify({"message": "Updated"})

@app.delete("/items/<item_id>")
def delete(item_id):
    delete_item(item_id)
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
