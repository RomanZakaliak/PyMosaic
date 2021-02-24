import os 
import logging
import jinja2
import aiohttp_jinja2
from aiohttp import web
import asyncio

from config import TEMPLATES_PATH, RESULT_FOLDER, THUMBNAILS_FOLDER
from views import SiteHandler
from router import setup_routes

#create Thumbnails and Result folder if it does not exists
def createFolders():
    if not os.path.exists(RESULT_FOLDER):
        os.mkdir(RESULT_FOLDER)
    if not os.path.exists(THUMBNAILS_FOLDER):
        os.mkdir(THUMBNAILS_FOLDER)

#setup Templates engine (Jinja)
def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_PATH))
    jinja2_env = aiohttp_jinja2.setup(app, loader = loader)
    return jinja2_env


async def init_app():
    #create app, maximal allowed upload size 3 * 1034 **2 = 3Mb
    app = web.Application(client_max_size=3 * 1024 ** 2)
    
    createFolders()

    setup_jinja(app)

    #create instance of Request handler
    handler = SiteHandler()

    #bind routes and request handler
    setup_routes(app, handler)

    return app

def main():
    logging.basicConfig(level=logging.DEBUG)

    host, port = "0.0.0.0", "5000"

    #Run app in async event loop
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    main()