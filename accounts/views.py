from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Reservation
from catalog.data_service import get_item, save_item

# ── AUTH ──────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome to Faust\'s Attic.')
        return redirect(request.GET.get('next', 'catalog'))
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'catalog'))
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('catalog')

# ── CART (session-based) ───────────────────────────────

def _get_cart(request):
    return request.session.get('cart', [])

def cart_add(request, item_id):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/?next=/item/{item_id}/')
    item = get_item(item_id)
    if not item:
        messages.error(request, 'Item not found.')
        return redirect('catalog')
    if item.get('is_sold') or item.get('is_reserved'):
        messages.warning(request, 'This item is no longer available.')
        return redirect('item_detail', item_id=item_id)
    cart = _get_cart(request)
    if item_id not in cart:
        cart.append(item_id)
        request.session['cart'] = cart
        messages.success(request, f'"{item["name"]}" added to your cart.')
    else:
        messages.info(request, 'This item is already in your cart.')
    return redirect('cart_view')

def cart_remove(request, item_id):
    cart = _get_cart(request)
    if item_id in cart:
        cart.remove(item_id)
        request.session['cart'] = cart
    return redirect('cart_view')

@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart_ids = _get_cart(request)
    items = [get_item(i) for i in cart_ids]
    items = [i for i in items if i]  # убираем None если предмет удалили
    total = sum(i['sell_price'] for i in items)
    return render(request, 'accounts/cart.html', {'items': items, 'total': total})

# ── RESERVATION ───────────────────────────────────────

@login_required(login_url='/accounts/login/')
def reserve(request, item_id):
    item = get_item(item_id)
    if not item:
        messages.error(request, 'Item not found.')
        return redirect('catalog')
    if item.get('is_sold') or item.get('is_reserved'):
        messages.warning(request, 'This item is no longer available for reservation.')
        return redirect('item_detail', item_id=item_id)

    # Создаём бронирование
    reservation = Reservation.objects.create(
        user       = request.user,
        item_id    = item_id,
        item_name  = item['name'],
        item_price = item['sell_price'],
    )

    # Помечаем предмет как забронированный в JSON
    item['is_reserved'] = True
    save_item(item)

    # Убираем из корзины
    cart = _get_cart(request)
    if item_id in cart:
        cart.remove(item_id)
        request.session['cart'] = cart

    return redirect('reservation_detail', code=reservation.code)

@login_required(login_url='/accounts/login/')
def reservation_detail(request, code):
    reservation = get_object_or_404(Reservation, code=code, user=request.user)
    return render(request, 'accounts/reservation_detail.html', {'r': reservation})

@login_required(login_url='/accounts/login/')
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'accounts/my_reservations.html', {'reservations': reservations})