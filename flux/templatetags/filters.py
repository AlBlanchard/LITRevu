from django import template

register = template.Library()


@register.filter
def full_stars(rating):
    """Renvoie une chaîne de caractères contenant le nombre d'étoiles pleines"""
    return "★" * rating


@register.filter
def empty_stars(rating):
    """Renvoie une chaîne de caractères contenant le nombre d'étoiles vides"""
    return "☆" * (5 - rating)
