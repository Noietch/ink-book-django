import asyncio
import websockets
from json import dumps


async def send_to_ws(team_id, data):
    ip = '43.138.71.90'
    port = '8888'
    try:
        async with websockets.connect(F"ws://{ip}:{port}/documents/{team_id}/") as websocket:
            await websocket.send(dumps({"type": "message", "message": data, "label": "database"}))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    team_id = 1
    asyncio.run(send_to_ws(team_id, {"data": "data"}))