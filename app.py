from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ap1-items')

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create_item():
    data = request.get_json()
    if not all(k in data for k in ("id", "name", "description")):
        return jsonify({"error": "Missing fields"}), 400
    table.put_item(Item=data)
    return jsonify({"message": "Item created", "item": data}), 201

@app.get("/items")
def list_items():
    resp = table.scan()
    return jsonify(resp.get("Items", [])), 200

@app.get("/items/<id>")
def get_item(id):
    try:
        resp = table.get_item(Key={"id": id})
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    item = resp.get("Item")
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item), 200

@app.put("/items/<id>")
def update_item(id):
    data = request.get_json()
    try:
        table.update_item(
            Key={"id": id},
            UpdateExpression="set #n=:n, description=:d",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={":n": data["name"], ":d": data["description"]},
        )
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Item updated"}), 200

@app.delete("/items/<id>")
def delete_item(id):
    try:
        table.delete_item(Key={"id": id})
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
