from decimal import Decimal
from django.conf import settings
from products.target import scrape_target_data
from products.walmart import scrape_walmart_data


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        product_keys = []
        cart = self.cart.copy()
        # get the product objects and add them to the cart
        for product_ids in product_ids:
            products = scrape_walmart_data(product_ids)

            if not products:
                products = scrape_target_data(product_ids)

            # for product_ids in product_ids:
            #     products = scrape_target_data(product_ids)
            try:
                for product in products:
                    # product_ids.append(cart[str(product['usItemId'])])
                    cart[str(product['usItemId'])]['product'] = product
                # cart[str(product['usItemId'])] = product
            except Exception as e:
                print(e)

        for product_key in cart.keys():
            product_keys.append(product_key)

        for item in cart.values():
            item['price'] = item['price']
            # item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):

        # print(product)

        # walmart_data =product['items']
        """
        Add a product to the cart or update its quantity.

        """
        try:
            for product in product:

                product_id = product['usItemId']
                # print(self.cart)
                if product_id not in self.cart:
                    self.cart[product_id] = {
                        'product': product,
                        'quantity': 0,
                        'price': str(product['price'])}
                if override_quantity:
                    self.cart[product_id]['quantity'] = quantity
                else:
                    self.cart[product_id]['quantity'] += quantity
            self.save()
        except Exception as e:
            print(e)

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price_walmart(self):

        value = sum(Decimal(product['price']) * product['quantity'] if product['product']
                                                                       ['product_brand'] == 'walmart' else 0 for product
                    in self.cart.values())

        return "{:.2f}".format(value)

    def get_total_price_target(self):

        value = sum(Decimal(product['price']) * product['quantity']
                    if product['product']['product_brand'] == 'target' else 0 for product in self.cart.values())

        return "{:.2f}".format(value)
