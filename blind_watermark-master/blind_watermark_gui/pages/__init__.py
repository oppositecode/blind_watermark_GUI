"""页面模块"""
from .home import create_home_page
from .embed import create_embed_page
from .extract import create_extract_page

__all__ = [
    'create_home_page',
    'create_embed_page', 
    'create_extract_page'
]
