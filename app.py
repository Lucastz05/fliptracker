from flask import Flask, jsonify, request, render_template
import json, os, uuid, datetime

app = Flask(__name__)
DATA_FILE = "data.json"

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify(load())

@app.route("/api/items", methods=["POST"])
def add_item():
    item = request.json
    item["id"] = str(uuid.uuid4())
    item["createdAt"] = datetime.datetime.now().isoformat()
    items = load()
    items.insert(0, item)
    save(items)
    return jsonify(item), 201

@app.route("/api/items/<id>", methods=["PUT"])
def update_item(id):
    items = load()
    for i, item in enumerate(items):
        if item["id"] == id:
            updated = request.json
            updated["id"] = id
            updated["createdAt"] = item.get("createdAt", "")
            items[i] = updated
            save(items)
            return jsonify(updated)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/items/<id>", methods=["DELETE"])
def delete_item(id):
    items = load()
    items = [i for i in items if i["id"] != id]
    save(items)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
