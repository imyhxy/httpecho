import os

import chardet
from aiohttp import web

TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)


def print_base(request: web.Request) -> None:
    print("Request:", repr(request))
    print("Headers:", dict(request.headers))


async def general(request: web.Request) -> web.Response:
    print_base(request)
    if request.can_read_body:
        content = await request.read()
        result = chardet.detect(content)
        if result["confidence"] >= 0.95:
            content = content.decode(result["encoding"])
        print("Content:", content[:200])

    return web.Response()


async def alarm_synch_alarm_infos(request: web.Request) -> web.Response:
    print_base(request)
    assert request.content_type == "application/x-www-form-urlencoded"
    print("Content:", (await request.text())[:200])
    return web.Response()


async def file_upload(request: web.Request) -> web.Response:
    print_base(request)
    assert request.content_type == "multipart/form-data"
    reader = await request.multipart()
    field = await reader.next()
    remain = 200
    while field is not None:
        if field.name == "file":
            print("Content: ", end="")
            with open(os.path.join(TEMP_DIR, field.filename), "wb") as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
                    if remain > 0:
                        print(chunk[:remain], end="")
                        remain = remain - len(chunk)
            print()
        else:
            print(f"Field: {field.name}, {field.filename}")

        field = await reader.next()

    return web.Response()


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/alarm/synchAlarmInfos", alarm_synch_alarm_infos)])
    app.add_routes([web.post("/uploadFile", file_upload)])
    app.add_routes([web.get("/{tail:.*}", general)])
    app.add_routes([web.post("/{tail:.*}", general)])

    web.run_app(app)
