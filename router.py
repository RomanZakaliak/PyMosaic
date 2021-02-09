from config import STATIC_PATH

def setup_routes(app, handler):
    router = app.router
    router.add_get('/', handler.index, name="index")
    router.add_static('/', path=STATIC_PATH, name='static')
