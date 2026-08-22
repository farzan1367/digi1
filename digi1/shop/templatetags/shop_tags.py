from django import template

register = template.Library()

# @register.simple_tag(
#     takes_context=True
# )
# def user_name(context):
#     user = context['request'].user
#     if user.is_authenticated:
#         return user.first_name + " " + user.last_name
#     return "مهمان"


@register.filter
def price_format(value):
    return "{:,}".format(value)
