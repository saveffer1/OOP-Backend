from src.main import app, initial_startup
import uvicorn

if __name__ == "__main__":
    initial_startup()
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)