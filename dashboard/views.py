from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from accounts.models import Reservation
from catalog.data_service import (
    get_items, get_item, save_item, delete_item,
    get_all_categories, get_all_eras,
    get_clients, get_sales
)
import uuid

STAFF_URL = '/dashboard/'


# ── OVERVIEW ──────────────────────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def overview(request):
    all_items   = get_items(show_sold=True)
    available   = [i for i in all_items if not i.get('is_sold') and not i.get('is_reserved')]
    reserved    = [i for i in all_items if i.get('is_reserved')]
    sold        = [i for i in all_items if i.get('is_sold')]
    pending_res = Reservation.objects.filter(status='pending').select_related('user')

    return render(request, 'dashboard/overview.html', {
        'counts': {
            'total':     len(all_items),
            'available': len(available),
            'reserved':  len(reserved),
            'sold':      len(sold),
        },
        'pending_reservations': pending_res,
    })


# ── ITEMS ─────────────────────────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def item_list(request):
    search    = request.GET.get('q', '')
    category  = request.GET.get('category', '')
    show_sold = request.GET.get('show_sold', '')

    items = get_items(
        category  = category or None,
        show_sold = True,
    )
    if search:
        items = [i for i in items if search.lower() in i.get('name', '').lower()]
    if not show_sold:
        items = [i for i in items if not i.get('is_sold')]

    return render(request, 'dashboard/item_list.html', {
        'items':      items,
        'categories': get_all_categories(),
        'search':     search,
        'category':   category,
        'show_sold':  show_sold,
    })


@staff_member_required(login_url='/accounts/login/')
@staff_member_required(login_url='/accounts/login/')
def item_form(request, item_id=None):
    item = get_item(item_id) if item_id else {}

    if request.method == 'POST':
        data = request.POST
        updated = {
            'id':          item.get('id') or f"item_{get_random_string(6)}",
            'name':        data.get('name', '').strip(),
            'category':    data.get('category', '').strip(),
            'era':         data.get('era', '').strip(),
            'country':     data.get('country', '').strip(),
            'condition':   data.get('condition', '').strip(),
            'buy_price':   float(data.get('buy_price') or 0),
            'sell_price':  float(data.get('sell_price') or 0),
            'year':        int(data.get('year') or 0),
            'provenance':  data.get('provenance', '').strip(),
            'description': data.get('description', '').strip(),
            'image':       item.get('image', ''),
            'is_sold':     item.get('is_sold', False),
            'is_reserved': item.get('is_reserved', False),
        }

        # Обработка загруженного фото
        photo = request.FILES.get('image')
        if photo:
            from catalog.data_service import save_item_image
            updated['image'] = save_item_image(updated['id'], photo)

        # Удалить фото если нажали «Remove photo»
        if data.get('remove_image') and updated['image']:
            from catalog.data_service import delete_item_image
            delete_item_image(updated['image'])
            updated['image'] = ''

        if not updated['name']:
            messages.error(request, 'Name is required.')
            return render(request, 'dashboard/item_form.html', {'item': updated})

        save_item(updated)
        messages.success(request, f'"{updated["name"]}" saved successfully.')
        return redirect('dashboard_items')

    return render(request, 'dashboard/item_form.html', {
        'item':       item,
        'categories': get_all_categories(),
        'eras':       get_all_eras(),
    })

@staff_member_required(login_url='/accounts/login/')
def item_mark_sold(request, item_id):
    item = get_item(item_id)
    if item:
        item['is_sold']     = True
        item['is_reserved'] = False
        save_item(item)
        # close any pending reservations for this item
        Reservation.objects.filter(item_id=item_id, status='pending').update(status='confirmed')
        messages.success(request, f'"{item["name"]}" marked as sold.')
    return redirect('dashboard_items')


@staff_member_required(login_url='/accounts/login/')
def item_delete(request, item_id):
    item = get_item(item_id)
    if request.method == 'POST' and item:
        delete_item(item_id)
        messages.success(request, f'"{item["name"]}" deleted.')
        return redirect('dashboard_items')
    return render(request, 'dashboard/item_confirm_delete.html', {'item': item})


# ── RESERVATIONS ──────────────────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def reservations(request):
    status = request.GET.get('status', '')
    qs = Reservation.objects.select_related('user').order_by('-created_at')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'dashboard/reservations.html', {
        'reservations': qs,
        'status_filter': status,
    })


@staff_member_required(login_url='/accounts/login/')
def reservation_confirm(request, pk):
    """Mark reservation as paid / confirmed."""
    res = Reservation.objects.get(pk=pk)
    res.status = 'confirmed'
    res.save()
    # mark item as sold in JSON
    item = get_item(res.item_id)
    if item:
        item['is_sold']     = True
        item['is_reserved'] = False
        save_item(item)
    messages.success(request, f'Reservation {res.code} confirmed. Item marked as sold.')
    return redirect('dashboard_reservations')


@staff_member_required(login_url='/accounts/login/')
def reservation_cancel(request, pk):
    res = Reservation.objects.get(pk=pk)
    res.status = 'cancelled'
    res.save()
    # free up the item
    item = get_item(res.item_id)
    if item:
        item['is_reserved'] = False
        save_item(item)
    messages.success(request, f'Reservation {res.code} cancelled. Item is available again.')
    return redirect('dashboard_reservations')


# ── CLIENTS ───────────────────────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def clients(request):
    return render(request, 'dashboard/clients.html', {
        'clients': get_clients(),
    })


# ── SALES ─────────────────────────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def sales(request):
    raw   = get_sales()
    items = {i['id']: i for i in get_items(show_sold=True)}
    for s in raw:
        s['item'] = items.get(s.get('item_id'), {})
    return render(request, 'dashboard/sales.html', {'sales': raw})