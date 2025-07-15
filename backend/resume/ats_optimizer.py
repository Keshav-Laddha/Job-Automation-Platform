# File: backend/resume/ats_optimizer.py
# Description: Optimizes resume points using BART model from HuggingFace (returns top 5-7 points)

from transformers import BartForConditionalGeneration, BartTokenizer
import torch

# Load BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def optimize_resume_points(resume_points, job_title, num_points=7):
    optimized_points = []

    for point in resume_points[:num_points]:
        prompt = f"Rewrite this resume point to align with the job title '{job_title}': {point}"

        inputs = tokenizer([prompt], max_length=512, return_tensors="pt", truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=100,
            early_stopping=True
        )
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        optimized_points.append(output)

    return optimized_points

# Example CLI usage
if __name__ == "__main__":
    job_title = "Software Engineer Intern at Microsoft"

    resume_points = [
        "Developed a web application using React and Flask.",
        "Built a REST API for handling user authentication and data storage.",
        "Optimized SQL queries to improve database performance.",
        "Led a 3-person team in delivering a college management system.",
        "Built a chatbot using Dialogflow integrated with a web app.",
        "Created a dashboard for real-time analytics using Plotly and Dash.",
        "Collaborated with a designer to improve UX for an edtech app."
    ]

    suggestions = optimize_resume_points(resume_points, job_title)
    
    print("🔍 Suggested Resume Points:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")