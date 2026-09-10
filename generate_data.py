import json
import time
from google import genai
from google.genai import types

# ضع الـ API Key الخاص بك هنا
client = genai.Client(api_key="AQ.Ab8RN6JvzOpguq_b6oMZlS30NheOjZQUEePbDdq73t0F1kMSbg")

# مثال لكتلة آيات: [start_surah, start_ayah, end_surah, end_ayah, start_global, end_global]
blocks_to_generate = [
    {"start_surah": 1, "start_ayah": 1, "end_surah": 1, "end_ayah": 7, "start_global": 1, "end_global": 7},
    {"start_surah": 2, "start_ayah": 1, "end_surah": 2, "end_ayah": 5, "start_global": 8, "end_global": 12},
    # يمكنك إضافة بقية المقاطع هنا
]

system_instruction = """
أنت خبير في التفسير والتدبر القرآني. مطلوب منك توليد تدبر للمقطع المرفق بالعامية المصرية الراقية مع التأصيل الشرعي والعمق العملي.
يجب أن ترجع النتيجة كـ JSON حصراً بالهيكل التالي:
{
  "title": "عنوان المقطع (مثال: 🔹 الفاتحة — أم الكتاب والسبع المثاني)",
  "quran_text": "النص القرآني للآيات",
  "deep_meaning": "الشرح الشامل والمعنى المعمق بالعامية المصرية الراقية مع الاستشهاد بأقوال المفسرين (ابن كثير، الشعراوي، إلخ)",
  "practical_wisdom": "💡 الحكمة العملية والعمل بالآية اليوم"
}
"""

results = []

for b in blocks_to_generate:
    prompt = f"قم بتوليد تدبر لسورة رقم {b['start_surah']} من آية {b['start_ayah']} إلى سورة رقم {b['end_surah']} آية {b['end_ayah']}"
    
    print(f"Generating block: {b['start_surah']}:{b['start_ayah']} - {b['end_surah']}:{b['end_ayah']}...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.3
        ),
    )
    
    data = json.loads(response.text)
    # دمج البيانات الأساسية مع النتيجة
    data.update(b)
    results.append(data)
    time.sleep(2) # مهلة بسيطة لتجنب تجاوز حد الطلبات

# حفظ النتائج في ملف JSON
with open('tadabbur_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("تم توليد البيانات وحفظها بنجاح!")
