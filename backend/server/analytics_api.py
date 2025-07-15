# analytics_api.py
from flask import Flask, jsonify, Blueprint
from backend.database.db import get_connection
from flask_cors import CORS

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/summary")
def get_summary():
    conn = None
    try:
        print("📊 Received request for analytics summary")
        conn = get_connection()
        cursor = conn.cursor()

        # Check if table exists first
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applied_jobs';")
        if not cursor.fetchone():
            print("⚠️ Table 'applied_jobs' does not exist")
            return jsonify({"applied": 0, "interview": 0, "offer": 0, "rejected": 0}), 200

        # Get status counts, normalizing case
        cursor.execute("SELECT LOWER(status) as status, COUNT(*) FROM applied_jobs GROUP BY LOWER(status)")
        data = cursor.fetchall()
        
        # Convert to dictionary with default values
        result = {"applied": 0, "interview": 0, "offer": 0, "rejected": 0}
        for status, count in data:
            if status in result:
                result[status] = count
        
        print(f"📊 Analytics data: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"🚨 Database error: {e}")
        # Return proper JSON error response
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@analytics_bp.route("/recent")
def get_recent_applications():
    """Get recent job applications"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT company, title, status, applied_at 
            FROM applied_jobs 
            ORDER BY applied_at DESC 
            LIMIT 5
        """)
        
        applications = []
        for row in cursor.fetchall():
            applications.append({
                "company": row[0],
                "title": row[1],
                "status": row[2],
                "applied_at": row[3]
            })
        
        return jsonify(applications)
        
    except Exception as e:
        print(f"🚨 Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()