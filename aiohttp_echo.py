from aiohttp import web


async def hello(request):
    print("Request:", repr(request))
    print("Headers:", dict(request.headers))
    print("Body   :", await request.text())

    return web.Response()


app = web.Application()
app.add_routes([web.get("/{tail:.*}", hello)])
app.add_routes([web.post("/{tail:.*}", hello)])

web.run_app(app)
