import datetime
from functools import lru_cache

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from products.target import scrape_target_data
from .cart import Cart
from .forms import CartAddProductForm
from products.walmart import scrape_walmart_data


@require_POST
def cart_add(request, usItemId):
    cart = Cart(request)
    product = scrape_walmart_data(usItemId)

    if not product:
        product = scrape_target_data(usItemId)

    # print(product)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        msg = product[0]['title'][:14]
    return redirect('/product/%s'%msg)


    # return render(request, 'product.html', {'scrape_walmart_data': product})


# @require_POST
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')

@lru_cache(30)
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True,
                                                                   }
                                                          )

    return render(request, 'cart/detail.html', {'cart': cart})

    # now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)
