from django import template

register = template.Library()

@register.filter
def has_liked(post, user):
    return post.liked_users.filter(id=user.id).exists()
