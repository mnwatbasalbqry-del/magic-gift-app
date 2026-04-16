from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# الصفحة الرئيسية: إما تعرض المولد أو تعرض الهدية إذا وجدت بيانات في الرابط
@app.route('/')
def index():
    return "<h1>السيرفر يعمل! أنا عباس العبقري</h1>"
    
    if name and date:
        # إذا كان الرابط يحتوي على بيانات، نعرض صفحة الشجرة
        return render_template('gift.html', name=name, date=date)
    
    # إذا كان الرابط فارغاً، نعرض صفحة إدخال البيانات (المولد)
    return render_template('generator.html')

# مسار معالجة البيانات وتوليد الباركود
@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    date = request.form.get('date')
    
    # بناء الرابط الذي سيتم تحويله لباركود
    # يقوم السيرفر بجلب رابط الموقع تلقائياً وإضافة المعلمات له
    base_url = request.url_root
    final_url = f"{base_url}?n={name}&d={date}"
    
    # إعدادات الباركود
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(final_url)
    qr.make(fit=True)
    
    # تلوين الباركود بنفس لون السمة (الوردي المحمر)
    img = qr.make_image(fill_color="#ff2b6b", back_color="white")
    
    # تحويل الصورة إلى صيغة يمكن عرضها في المتصفح مباشرة (Base64)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('result.html', name=name, url=final_url, qr_code=qr_base64)

if __name__ == '__main__':
    # تشغيل التطبيق (Debug=True للتطوير فقط)
    app.run(debug=True)
