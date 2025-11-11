from flask import Flask, request, jsonify
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)

print("🚀 Thermal AI Server - Ready!")
print("✅ Endpoints: /, /status, /analyze")

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "service": "Thermal AI Cloud Server",
        "version": "2.0",
        "endpoints": {
            "/analyze": "POST - Analyze thermal data",
            "/status": "GET - Server status",
            "/": "GET - Home page"
        }
    })

@app.route("/status")
def status():
    return jsonify({
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
        "service": "Thermal AI"
    })

@app.route("/analyze", methods=["POST"])
def analyze_thermal():
    try:
        data = request.json
        thermal_data = data.get("thermal_data", [])
        sensor_id = data.get("sensor_id", "unknown")
        location = data.get("location", "unknown")
        
        print(f"📡 Received data from {sensor_id} at {location}")
        print(f"📊 Data points: {len(thermal_data)}")
        
        if len(thermal_data) >= 64:
            # تحويل البيانات إلى مصفوفة 8x8
            matrix = np.array(thermal_data).reshape(8, 8)
            min_temp = np.min(matrix)
            max_temp = np.max(matrix)
            avg_temp = np.mean(matrix)
            
            # خوارزمية كشف التسريبات المتقدمة
            leak_probability = 0.0
            
            # 1. كشف المناطق الباردة
            cold_spots = matrix < 18
            cold_count = np.sum(cold_spots)
            
            # 2. كشف التدرجات الحادة
            grad_x, grad_y = np.gradient(matrix)
            total_gradient = np.sqrt(grad_x**2 + grad_y**2)
            max_gradient = np.max(total_gradient)
            
            # حساب احتمالية التسريب
            if cold_count > 5:
                leak_probability = 0.95
            elif cold_count > 3 and max_gradient > 2.0:
                leak_probability = 0.8
            elif min_temp < 16:
                leak_probability = 0.7
            elif min_temp < 18:
                leak_probability = 0.4
            elif cold_count > 2:
                leak_probability = 0.3

            # إعداد الرد
            response = {
                "status": "success",
                "leak_probability": leak_probability,
                "analysis": {
                    "min_temperature": float(min_temp),
                    "max_temperature": float(max_temp),
                    "average_temperature": float(avg_temp),
                    "cold_spots": int(cold_count),
                    "risk_level": "high" if leak_probability > 0.7 else "medium" if leak_probability > 0.4 else "low"
                },
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Analysis complete - Leak probability: {leak_probability:.1%}")
            return jsonify(response)
        else:
            return jsonify({
                "status": "error",
                "message": "Insufficient data. Need 64 thermal points."
            }), 400
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Server starting on port {port}")
    print("📍 Ready for thermal data analysis!")
    app.run(host="0.0.0.0", port=port, debug=False)
