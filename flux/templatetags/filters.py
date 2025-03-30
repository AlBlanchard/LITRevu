from django import template

register = template.Library()


@register.filter
def full_stars(rating):
    """Renvoie une chaîne de caractères contenant le nombre d'étoiles pleines"""
    rating = int(rating)
    return "★" * rating


@register.filter
def empty_stars(rating):
    """Renvoie une chaîne de caractères contenant le nombre d'étoiles vides"""
    rating = int(rating)
    return "☆" * (5 - rating)
