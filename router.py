from config import STATIC_PATH

def setup_routes(app, handler):
    router = app.router
    router.add_get('/', handler.index, name='index')
    router.add_post('/upload_file', handler.upload_file, name='upload_file')
    router.add_get('/download/{filename}', handler.download, name='download')
    router.add_static('/', path=STATIC_PATH, name='static')
