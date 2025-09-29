from products.models import Product_group

def product_groups(request):
    return {
        "product_groups_navbar": Product_group.objects.filter(in_navbar=True).order_by("order")
    }