from flask import Flask, request, jsonify, render_template, redirect
from transformers import BartForConditionalGeneration, BartTokenizer
import torch
from flask_cors import CORS
from backend.server.analytics_api import analytics_bp
from backend.database.db import init_db
from backend.server.applied_jobs_api import applied_jobs_bp  # You need to create this blueprint
from backend.server.job_api import job_api_bp
import os

app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:3000", 
    "https://profound-jointly-thrush.ngrok-free.app"
], supports_credentials=True)

# Initialize database on startup
init_db()

app.config["UPLOAD_FOLDER"] = "backend/uploads"

# Register analytics blueprint
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(applied_jobs_bp)
app.register_blueprint(job_api_bp)

# Load BART model
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def generate_bart_response(resume_point, job_title, job_description=""):
    prompt = f"""
Given the job title '{job_title}' and job description: {job_description if job_description else '(not provided)'}, 
rewrite the following resume point to better align with the role:
{resume_point}
    """
    inputs = tokenizer([prompt], max_length=512, return_tensors="pt", truncation=True)

    output_ids = model.generate(
        inputs["input_ids"],
        num_beams=5,
        num_return_sequences=5,
        max_length=100,
        early_stopping=True
    )

    return [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]

@app.route("/optimize", methods=["GET"])
def optimize_form():
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    query = request.query_string.decode()
    if query:
        return redirect(f"{frontend_url}/optimize?{query}")
    else:
        return redirect(f"{frontend_url}/optimize")

@app.route("/optimize", methods=["POST"])
def optimize_resume():
    data = request.get_json()
    job_title = data.get("job_title", "")
    job_description = data.get("job_description", "")
    resume_points = data.get("resume_points", "")

    if not job_title or not resume_points:
        return jsonify({"error": "Missing job_title or resume_points"}), 400

    # Split multiple points (by newline, bullet, or dash)
    bullets = [b.strip("•- \n") for b in resume_points.strip().split("\n") if b.strip()]

    optimized = []
    for point in bullets:
        suggestions = generate_bart_response(point, job_title, job_description)
        optimized.append({
            "original": point,
            "suggestions": suggestions
        })

    return jsonify({"optimized_points": optimized})

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AI Job Assistant API is running"})

if __name__ == "__main__":
    app.run(debug=True, port=5002)