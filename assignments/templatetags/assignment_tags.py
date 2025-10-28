from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def course_image_url(course_code):
    """Maps course codes to Unsplash image URLs."""
    image_urls = {
        'csc101': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80',  # Programming
        'mat101': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80',  # Math
        'phy101': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=800&q=80',  # Physics
        'chm101': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80',  # Chemistry
        'bio101': 'https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&w=800&q=80',  # Biology
        'eng101': 'https://images.unsplash.com/photo-1581094283645-9f6fbcef9cab?auto=format&fit=crop&w=800&q=80',  # Engineering
        'lit101': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=800&q=80',  # Literature
        'his101': 'https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=800&q=80',  # History
    }
    
    # Default image if course code not found
    default_url = 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80'
    return image_urls.get(course_code.lower(), default_url)