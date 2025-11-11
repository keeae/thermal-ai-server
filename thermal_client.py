import requests
import time
import random
from datetime import datetime

# 🔗 رابط السيرفر الجديد - سيتم تعبئته بعد النشر
SERVER_URL = "https://YOUR-NEW-SERVER.onrender.com/analyze"

print("🌐 عميل الكاميرا الحرارية - جاهز للتشغيل")
print("📍 بعد نشر السيرفر، غيّر SERVER_URL بالرابط الجديد")
print()

class ThermalClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.cycle_count = 0
        
    def check_connection(self):
        """فحص الاتصال بالسيرفر"""
        try:
            base_url = self.server_url.replace("/analyze", "/status")
            response = requests.get(base_url, timeout=10)
            if response.status_code == 200:
                print("✅ الاتصال ناجح! السيرفر شغال")
                return True
            else:
                print(f"❌ خطأ في السيرفر: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ فشل الاتصال: {e}")
            return False
    
    def create_thermal_data(self):
        """إنشاء بيانات حرارية واقعية"""
        base_temp = 25.0
        data = []
        
        for i in range(8):
            for j in range(8):
                # نمط حراري طبيعي
                distance = ((i-3.5)**2 + (j-3.5)**2)**0.5
                temp_variation = -distance * 0.3
                temperature = base_temp + temp_variation + random.uniform(-1, 1)
                data.append(round(temperature, 2))
        
        # محاكاة تسريب مياه في 25% من الدورات
        if random.random() < 0.25:
            print("💧 محاكاة تسريب مياه...")
            for i in range(3, 6):
                for j in range(3, 6):
                    idx = i * 8 + j
                    data[idx] = max(16.0, data[idx] - random.uniform(6, 9))
                
        return data
    
    def send_to_server(self, thermal_data):
        """إرسال البيانات للسيرفر"""
        try:
            payload = {
                "thermal_data": thermal_data,
                "timestamp": datetime.now().isoformat(),
                "sensor_id": "thermal_camera_01",
                "location": "الموقع الرئيسي"
            }
            
            response = requests.post(self.server_url, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                leak_prob = result.get("leak_probability", 0)
                
                if leak_prob > 0.8:
                    print(f"🚨 إنذار عالي! تسريب مياه: {leak_prob:.1%}")
                elif leak_prob > 0.6:
                    print(f"⚠️ تحذير! اشتباه تسريب: {leak_prob:.1%}")
                else:
                    print(f"✅ طبيعي: {leak_prob:.1%}")
                    
                return True
            else:
                print(f"❌ خطأ في السيرفر: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ فشل الاتصال: {e}")
            return False
    
    def run_test(self):
        """تشغيل اختبار سريع"""
        if not self.check_connection():
            return
        
        print("🚀 بدء الاختبار...")
        
        for i in range(3):
            self.cycle_count += 1
            print(f"\n🔄 الدورة #{self.cycle_count}")
            
            thermal_data = self.create_thermal_data()
            min_temp = min(thermal_data)
            max_temp = max(thermal_data)
            
            print(f"📊 البيانات: {len(thermal_data)} نقطة")
            print(f"🌡️ المدى: {min_temp:.1f}°C - {max_temp:.1f}°C")
            
            self.send_to_server(thermal_data)
            time.sleep(3)
        
        print("\n✅ انتهى الاختبار")

if __name__ == "__main__":
    client = ThermalClient(SERVER_URL)
    print("🔧 تذكر: غيّر SERVER_URL برابط السيرفر الجديد بعد النشر")
    print("💡 مثال: https://thermal-server-v2.onrender.com")
    print()
    client.run_test()
