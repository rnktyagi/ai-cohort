from fastapi import FastAPI 
app = FastAPI(title="FastAPI Health API") 
@app.get("/health") 
def health(): 
    return {"status": "ok"}