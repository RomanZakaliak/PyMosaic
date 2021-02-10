import io
import asyncio
import aiohttp_jinja2
from aiohttp import web
from src.image import ImageTransform
from config import RESULT_FOLDER

class SiteHandler:

    @aiohttp_jinja2.template('index.html.jinja')
    async def index(self, request):
        return {}
    
    async def upload_file(self, request):
        #post_id = request.match_info['post']
        post = await request.post()
        image = post.get('file')
        chunk_size = int(post.get('chunk_size'))
        if not image or not chunk_size:
            return web.json_response({'error':'error receiving image data, please try again'})

        if image:
            img_content = image.file.read()
            await self.handle_image(img_content, image.filename, chunk_size)
        return web.json_response({'filename':str(image.filename)})

    async def handle_image(self, img_content, filename, chunk_size):
        buf = io.BytesIO(img_content)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.make_transform, buf, filename, chunk_size)

    def make_transform(self, buf, filename, chunk_size):
        img = ImageTransform(buf)
        img.open_file()
        img.divide_onto_chunks(chunk_size=chunk_size)
        img.save_new_file(destination=RESULT_FOLDER, output_file_name=filename)

    async def download(self, request):
        filename = request.match_info['filename']
        return web.Response(body=f'{RESULT_FOLDER}/{filename}')



    
