import io
import asyncio
import aiohttp_jinja2
from aiohttp import web
from multidict import MultiDict
from src.image import Pixelize
from PIL import Image
from config import RESULT_FOLDER, THUMBNAILS_FOLDER

class SiteHandler:

    @aiohttp_jinja2.template('index.html.jinja')
    async def index(self, request):
        return {}
    
    async def upload_file(self, request):
        post = await request.post()
        image = post.get('file')
        chunk_size = int(post.get('chunk_size'))

        keys = ['x1', 'y1', 'x2', 'y2']
        coords = dict()
        for key in keys:
            coords[key] = int(float(post.get(key)))
        coords = SiteHandler.correct_coords(coords)

        if not image or not chunk_size:
            return web.json_response({'error':'error receiving image data, please try again'})

        if image:
            img_content = image.file.read()
            await self.handle_image(img_content, coords,  image.filename, chunk_size)
        return web.json_response({'filename':str(image.filename)})

    async def handle_image(self, img_content, coords, filename, chunk_size):
        buf = io.BytesIO(img_content)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.make_transform, buf, coords, filename, chunk_size)

    def make_transform(self, buf, coords, filename, chunk_size):
        img = Pixelize(buf)
        img.divide_onto_chunks(coords, chunk_size)
        img.save_new_file(thumb_destination=THUMBNAILS_FOLDER, destination=RESULT_FOLDER, output_file_name=filename)

    async def download(self, request):
        filename = request.match_info['filename']
        image_file = Image.open(f'{RESULT_FOLDER}/{filename}')
        file_bytes = io.BytesIO()
        image_file.save(file_bytes, image_file.format)
        return web.Response(
            headers=MultiDict({'Content-Disposition': 'Attachment'}),
            body=file_bytes.getvalue())

    @staticmethod
    def correct_coords(coords: dict)->dict:
        if coords['x1'] > coords['x2']:
            coords['x1'], coords['x2'] = coords['x2'], coords['x1']

        if coords['y1'] > coords['y2']:
            coords['y1'], coords['y2'] = coords['y2'], coords['y1']

        return coords



    
