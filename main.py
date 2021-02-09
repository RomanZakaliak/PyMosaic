import logging
import jinja2
import aiohttp_jinja2
from aiohttp import web
import asyncio

from config import TEMPLATES_PATH
from views import SiteHandler
from router import setup_routes

def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_PATH))
    jinja2_env = aiohttp_jinja2.setup(app, loader = loader)
    return jinja2_env

async def init_app():
    app = web.Application()
    setup_jinja(app)

    handler = SiteHandler()

    setup_routes(app, handler)
    host, port = "127.0.0.1","5000"

    return app, host, port

def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app())
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    main()