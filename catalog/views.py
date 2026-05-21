from django.shortcuts import render, redirect
from .data_service import get_items, get_item, get_all_categories, get_all_eras

def catalog(request):
    category  = request.GET.get("category", "")
    era       = request.GET.get("era", "")
    max_price = request.GET.get("max_price", "")

    items = get_items(
        category  = category  or None,
        era       = era       or None,
        max_price = max_price or None,
    )
    return render(request, "catalog/catalog.html", {
        "items":      items,
        "categories": get_all_categories(),
        "eras":       get_all_eras(),
        "selected":   {"category": category, "era": era, "max_price": max_price},
    })

def item_detail(request, item_id):
    item = get_item(item_id)
    if not item:
        return redirect("catalog")
    return render(request, "catalog/item_detail.html", {"item": item})

def contacts(request):
    return render(request, "catalog/contacts.html")