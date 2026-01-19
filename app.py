from fastapi import FastAPI, BackgroundTasks
from send_emails import send_emails_function
from process_replies import process_replies_function
import os
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import io

app = FastAPI(title="School Email Automation API")
app.mount("/static", StaticFiles(directory="static"), name="static")
# ===============================
# HOME ROUTE
@app.get("/")
def home():
    return FileResponse("static/index.html")

# ===============================
# SEND EMAILS API
# ===============================
@app.post("/send-emails")
def send_emails(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_emails_function)
    return {
        "status": "success",
        "message": "Email sending started in background"
    }
@app.get("/logs/sent-emails")
def get_sent_emails():
    log_file = "logs/sent_emails.log"
    if not os.path.exists(log_file):
        return []

    with open(log_file, "r") as f:
        return [line.strip() for line in f.readlines()]
# ===============================
# PROCESS REPLIES API
# ===============================
@app.post("/process-replies")
def process_replies(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_replies_function)
    return {
        "status": "success",
        "message": "Reply processing started in background"
    }
@app.get("/logs/replies")
def get_replies():
    log_file = "logs/replies.log"
    if not os.path.exists(log_file):
        return []

    with open(log_file, "r") as f:
        return [line.strip() for line in f.readlines()]
# ===============================
# RUN BOTH
# ===============================
@app.post("/run-all")
def run_all(background_tasks: BackgroundTasks):
    # mark system as running
    os.makedirs("logs", exist_ok=True)
    with open("logs/status.txt", "w") as f:
        f.write("running")

    def full_workflow():
        send_emails_function()
        process_replies_function()
        with open("logs/status.txt", "w") as f:
            f.write("completed")

    background_tasks.add_task(full_workflow)

    return {
        "status": "success",
        "message": "Full automation started"
    }
@app.get("/status")
def get_status():
    status_file = "logs/status.txt"
    if not os.path.exists(status_file):
        return {"status": "idle"}

    with open(status_file, "r") as f:
        return {"status": f.read().strip()}

@app.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    if not file.filename.endswith(".xlsx"):
        return {"error": "Only Excel files allowed"}

    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    background_tasks.add_task(send_emails_function, df)

    return {
        "status": "success",
        "message": "Emails started from uploaded Excel"
    }
