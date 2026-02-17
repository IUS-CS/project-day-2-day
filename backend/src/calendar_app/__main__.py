from fastapi import FastAPI
from calendar_app.api.hello_api import router as hello_router

app = FastAPI()
app.include_router(hello_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("calendar_app.__main__:app", reload=True)