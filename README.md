# DivineBeauty 💄🛍️

DivineBeauty یک فروشگاه آنلاین محصولات زیبایی و آرایشی است که با استفاده از فریم‌ورک Django توسعه داده شده و از قابلیت‌های پیشرفته‌ای مانند احراز هویت ایمیل، سیستم OTP، Docker، Celery و موارد دیگر بهره می‌برد.

---

## ✨ ویژگی‌ها

- ثبت‌نام و ورود کاربران با تأیید ایمیل
- ارسال کد تأیید (OTP) با Celery
- پنل کاربری با قابلیت مشاهده پروفایل
- مدیریت کاربران در پنل ادمین Django
- ساختار ماژولار و تمیز برای توسعه بهتر
- پشتیبانی از Docker برای اجرا در محیط‌های استاندارد
- ساختار آماده برای استفاده در سرورهای تولیدی (supervisord, gunicorn)
- استفاده از cloudinary برای ذخیره عکس ها
- اتصال به دیتابیس postgres در سرور جداگانه

---

## 🛠️ تکنولوژی‌ها

- Python 3.x
- Django
- PostgreSQL (قابل تنظیم)
- Celery + Redis (برای ارسال OTP)
- Docker
- HTML / CSS (با استفاده از قالب‌های ساده)
- REST API (با استفاده از Django REST Framework)

---

## دیدن سایت 
- سایت روی سرور رایگان آپلود شده ۳۰ ثاینه صبر کنید تا سایت لود شود
- لینک سایت https://divinesite-latest.onrender.com

---

## ⚙️ نحوه اجرا (لوکال)

### 1. کلون کردن مخزن:
```bash
git clone https://github.com/Sajjadhosseinrezaei/DivineBeauty.git
cd DivineBeauty
```

### 2. ساخت محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate
```

### 3. نصب پیش‌نیازها:
- نیاز به تغییر تنظیمات دیتابیس در فایل settings.py برای اجرا در حالت لوکال
- نیاز به ست کردن فضای storage در settings.py
```bash
pip install -r requirements.txt
```

### 4. اعمال مهاجرت‌ها و اجرای سرور:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 5. ساخت کاربر ادمین:
```bash
python manage.py createsuperuser
```

---

## 🐳 اجرا با Docker (اختیاری)

```bash
docker build -t divine-beauty .
docker run -p 8000:8000 divine-beauty
```

---

## 📂 ساختار پروژه

```
DivineBeauty/
├── A/                      # تنظیمات پروژه Django
├── accounts/               # اپ مربوط به ثبت‌نام، ورود و کاربران
├── home/                   # صفحه اصلی
├── templates/              # قالب‌های HTML
├── static/                 # فایل‌های استاتیک
├── Dockerfile              # فایل Docker
├── requirements.txt        # پکیج‌های پایتون
├── manage.py
```

---

## 📧 تماس با من

برای سؤال یا همکاری، می‌توانید در [GitHub](https://github.com/Sajjadhosseinrezaei) با من در ارتباط باشید.
