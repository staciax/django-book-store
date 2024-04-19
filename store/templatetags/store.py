from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import template
from django.template.loader import get_template

if TYPE_CHECKING:
    from store.models import Product

register = template.Library()


@register.simple_tag
def text_field(
    label: str,
    type: str,
    name: str,
    disabled: bool = False,
    required: bool = False,
    **kwargs: dict[str, Any],
) -> str:
    template = get_template('store/ui/text-field.html')
    context = {
        'label': label,
        'name': name,
        'type': type,
        **kwargs,
    }
    if disabled:
        context['disabled'] = 'disabled'
    if required:
        context['required'] = 'required'
    return template.render(context=context)


@register.simple_tag
def button(
    label: str,
    type: str = 'submit',
    font: str = 'font-extralight',
    text: str = 'text-base',
    disabled: bool = False,
) -> str:
    template = get_template('store/ui/button.html')
    context = {
        'label': label,
        'type': type,
        'font': font,
        'text': text,
    }
    if disabled:
        context['disabled'] = 'disabled'
    return template.render(context=context)


@register.simple_tag
def button_light(label: str, type: str = 'submit') -> str:
    template = get_template('store/ui/button-light.html')
    context = {
        'label': label,
        'type': type,
    }
    return template.render(context=context)


@register.simple_tag
def product_card(product: Product, csrf_token: str) -> str:
    template = get_template('store/ui/product-card.html')
    context = {
        'product': product,
        'csrf_token': csrf_token,
    }
    return template.render(context=context)
