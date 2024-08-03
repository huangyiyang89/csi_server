from fastapi import APIRouter, WebSocketDisconnect, WebSocket
import asyncio

router = APIRouter(prefix="/api/streamings")


@router.websocket("/rtspws")
async def websocket_streaming(websocket: WebSocket, url: str):
    await websocket.accept()
    command = [
        "ffmpeg",
        "-i",
        url,  # Input
        "-rtsp_transport",
        "tcp",
        "-f",
        "flv",  # Output format
        "-c",
        "copy",  # Codec
        "pipe:",  # Output to stdout
    ]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        while True:
            packet = await process.stdout.read(8192)
            if not packet:
                print("packet is none")
                await websocket.send_bytes(b'\x00\x00\x00\x00')
                break
            await websocket.send_bytes(packet)
    except WebSocketDisconnect:
        print("WebSocketDisconnect")
    except asyncio.TimeoutError:
        print("asyncio timeout")
    except Exception as e:
        print(f"unknown error: {e}")
    finally:
        process.terminate()
        await process.wait()
        await websocket.close()
