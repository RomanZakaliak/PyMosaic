import aiohttp_jinja2
from aiohttp import web

class SiteHandler:

    @aiohttp_jinja2.template('index.html.jinja')
    async def index(self, request):
        return {}
    
    #async def upload_file(self, request):