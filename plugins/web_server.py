from aiohttp import web

async def web_server():
    async def handle(request):
        return web.Response(text="Telegram Bot is Running!")

    app = web.Application()
    app.router.add_get("/", handle)
    return app
