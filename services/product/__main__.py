from fastapi import FastAPI
import uvicorn

from controllers import router

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
