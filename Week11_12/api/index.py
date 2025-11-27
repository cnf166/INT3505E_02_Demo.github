from main import app
import uvicorn

def handler(event, context):
    return uvicorn.run(app, host="0.0.0.0", port=8000)