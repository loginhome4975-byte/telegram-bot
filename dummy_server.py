from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

def create_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app
