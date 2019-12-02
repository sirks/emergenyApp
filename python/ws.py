import asyncio
import pathlib
import ssl
from time import time

import websockets

from python import loop
from python.server import sosses


async def listen(websocket, path):
    last_sos_check = 0
    while True:
        if last_sos_check < sosses['time']:
            last_sos_check = time()
            await websocket.send(sosses['locations'])
        await asyncio.sleep(1)


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name('cert.pem')
ssl_context.load_cert_chain(localhost_pem)

start_ws = websockets.serve(listen, "0.0.0.0", 4000, ssl=ssl_context)

if __name__ == '__main__':
    loop.run_until_complete(start_ws)
