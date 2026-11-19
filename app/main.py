from fastapi import FastAPI

app = FastAPI(title="Suhail API")


@app.get("/health")
def health():
    return {"status": "ok"}