from django import template

# register=template.Library()

# @register.simple_tag(name='gettotal')

# def gettotal(cart):
#     total=0
#     for item in cart.added_items.all():
#         total+=item.service.price    
#     return total



# from django import template

# register = template.Library()

# @register.simple_tag
# def gettotal(cart_items):
#     return sum(item.service.price for item in cart_items)


from django import template

register = template.Library()

@register.simple_tag
def gettotal(cart_items):
    return sum(item.service.price for item in cart_items if item.service is not None)
