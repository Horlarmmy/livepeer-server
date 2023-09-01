import asyncio
import websockets
import subprocess

# WebSocket server configuration
HOST = "localhost"
PORT = 8080

# GStreamer pipeline
pipeline = (
    "gst-launch-1.0 -v fdsrc ! h264parse ! flvmux ! rtmpsink location="
)

async def handle_connection(websocket, path):
    print("Client connected")
    try:
        # Extract the rtmpUrl from the path
        rtmp_url = path
        full_pipeline = pipeline + rtmp_url

        # Start GStreamer pipeline
        gstreamer_process = subprocess.Popen(
            full_pipeline, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #text=True  # For working with text-based output
        )

        async for message in websocket:
            if not message:
                break
            print("Received message from client:", len(message), "bytes")
            gstreamer_process.stdin.write(message)
            gstreamer_process.stdin.flush()

        # Capture and print stderr output
        for line in gstreamer_process.stderr:
            print("GStreamer STDERR:", line.strip())

    except websockets.ConnectionClosed:
        gstreamer_process.kill()
        print("Client disconnected")

start_server = websockets.serve(handle_connection, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
