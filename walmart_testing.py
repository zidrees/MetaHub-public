from wapy.api import Wapy

wapy = Wapy("a4e25ee3c0mshe6ab478732e48ebp1bcaa6jsna2071ec6b2d4")  # Create an instance of Wapy.

# #### PRODUCT LOOKUP ####
# product = wapy.product_lookup('21853453')  # Perform a product lookup using the item ID.
# print(product.name)  # Apple EarPods with Remote and Mic MD827LLA
# print(product.weight)  # 1.0
# print(product.customer_rating)  # 4.445
# print(product.medium_image)  # https://i5.walmartimages.com/asr/6cd9c...

#### PRODUCT SEARCH ####
products = wapy.search('xbox')
for product in products:
    print(product.name)
