import boto3
import uuid

region = "us-east-1"
table_name = "ap1-items"
dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(table_name)

def create_item(nombre, precio, categoria):
    item_id = str(uuid.uuid4())
    table.put_item(Item={
        "id": item_id,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria
    })
    return item_id

def get_item(item_id):
    return table.get_item(Key={"id": item_id}).get("Item")

def list_items():
    return table.scan().get("Items", [])

def update_item(item_id, data):
    update_expr = "SET " + ", ".join([f"{k}=:{k}" for k in data])
    expr_vals = {f":{k}": v for k, v in data.items()}
    table.update_item(Key={"id": item_id}, UpdateExpression=update_expr,
                      ExpressionAttributeValues=expr_vals)

def delete_item(item_id):
    table.delete_item(Key={"id": item_id})
