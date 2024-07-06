from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def cart_summary(request):
    #Get the cart   
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    if request.method == 'POST' and request.POST.get('action') == 'post':
        if request.user.is_authenticated:
            cart = Cart(request)
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity})
            messages.success(request, "Product added to cart.")
            return response
        else:
            return HttpResponseForbidden("You must log in to add items to your cart.")
    else:
        return HttpResponseForbidden("Invalid request.")
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)
                    
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item Deleted From Shopping Cart...."))
        return response
        #return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Your Cart Has Been Updated...."))
        return response
        #return redirect('cart_summary')
