from cat.mad_hatter.decorators import plugin, hook
from bs4 import BeautifulSoup
from .service import HTMLParser
from .settings import Settings

@plugin
def settings_model():
    return Settings

@hook
def rabbithole_instantiates_parsers(file_handlers, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    file_handlers["text/html"] = HTMLParser(settings=settings)

    return file_handlers
