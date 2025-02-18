from fastapi import FastAPI
from routes import email, leads, meetings

app = FastAPI(title="AI Business Assistant")

# Include routes
app.include_router(email.router, prefix="/email")
app.include_router(leads.router, prefix="/leads")
app.include_router(meetings.router, prefix="/meetings")

@app.get("/")
def home():
    return {"message": "AI Business Assistant Running"}
