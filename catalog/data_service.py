import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def _load(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _save(filename, data):
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── ПРЕДМЕТЫ ──────────────────────────────────────────
def get_items(category=None, era=None, max_price=None, show_sold=False):
    items = _load("items.json")
    if not show_sold:
        items = [i for i in items if not i.get("is_sold")]
    if category:
        items = [i for i in items if i.get("category") == category]
    if era:
        items = [i for i in items if i.get("era") == era]
    if max_price:
        items = [i for i in items if i.get("sell_price", 0) <= float(max_price)]
    return items

def get_item(item_id):
    items = _load("items.json")
    return next((i for i in items if i["id"] == item_id), None)

def get_all_categories():
    items = _load("items.json")
    return sorted(set(i["category"] for i in items if i.get("category")))

def get_all_eras():
    items = _load("items.json")
    return sorted(set(i["era"] for i in items if i.get("era")))

def save_item(item):
    items = _load("items.json")
    for idx, existing in enumerate(items):
        if existing["id"] == item["id"]:
            items[idx] = item
            _save("items.json", items)
            return
    items.append(item)
    _save("items.json", items)

def delete_item(item_id):
    items = _load("items.json")
    items = [i for i in items if i["id"] != item_id]
    _save("items.json", items)

# ── КЛИЕНТЫ ───────────────────────────────────────────
def get_clients():
    return _load("clients.json")

def get_client(client_id):
    clients = _load("clients.json")
    return next((c for c in clients if c["id"] == client_id), None)

# ── ПРОДАЖИ ───────────────────────────────────────────
def get_sales():
    return _load("sales.json")