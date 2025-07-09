# DivineBeauty 💄🛍️

DivineBeauty یک فروشگاه آنلاین محصولات زیبایی و آرایشی است که با استفاده از فریم‌ورک Django توسعه داده شده و از قابلیت‌های پیشرفته‌ای مانند احراز هویت ایمیل، سیستم OTP، Docker، Celery و موارد دیگر بهره می‌برد.

---

## ✨ ویژگی‌ها

- ثبت‌نام، ورود و خروج کاربران با JWT
- تأیید ایمیل با ارسال کد OTP
- امکان ارسال مجدد OTP
- پروفایل کاربری و مشاهده اطلاعات حساب
- لیست و ساخت کاربران از طریق API
- جستجوی محصولات و فیلتر بر اساس دسته‌بندی
- صفحات عمومی مانند درباره ما و سوالات متداول
- سیستم کامل سبد خرید و پرداخت
- کامنت‌گذاری و حذف نظر برای محصولات
- API کامل برای محصولات
- ذخیره‌سازی ابری عکس‌ها با Cloudinary
- تنظیمات پویا از پنل ادمین با Constance
- ذخیره لاگ خطاها در فایل `django_error.log`
- پشتیبانی از Docker برای اجرا در محیط‌های استاندارد
- استفاده از WhiteNoise برای فایل‌های استاتیک در حالت production

---

## 🛠️ تکنولوژی‌های استفاده‌شده

- Python 3.x
- Django 5.1.x
- PostgreSQL
- Django REST Framework
- Celery + Redis
- JWT (SimpleJWT)
- Cloudinary
- Docker
- Constance
- dotenv
- WhiteNoise

---

## 🌐 لینک دمو

سایت روی سرور رایگان (Render) دیپلوی شده و ممکن است حدود ۱ دقیقه برای بالا آمدن زمان ببرد:

🔗 [مشاهده سایت](https://divinesite-latest.onrender.com)

---
## 🖼 پیش‌نمایش رابط کاربری

![نمای ۱](Screenshot%20from%202025-06-29%2014-41-28.png)
![نمای ۲](Screenshot%20from%202025-06-29%2014-41-44.png)
![نمای ۳](Screenshot%20from%202025-06-29%2014-41-50.png)
![نمای ۱](Screenshot%20from%202025-07-08%2016-54-41.png)
![نمای ۲](Screenshot%20from%202025-07-08%2016-55-31.png)
![نمای ۳](Screenshot%20from%202025-07-08%2016-55-40.png)
![نمای ۴](Screenshot%20from%202025-07-08%2016-57-37.png)
![نمای ۵](Screenshot%20from%202025-07-08%2016-58-02.png)






## 🧪 نحوه اجرا (لوکال)

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

### 3. نصب پکیج‌ها:
```bash
pip install -r requirements.txt
```

### 4. تنظیم فایل `.env`:
نمونه متغیرهای موردنیاز:
```
DATABASE_URL=postgres://user:password@host:5432/dbname
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
CELERY_BROKER_URL=redis://localhost:6379/0
```

### 5. اعمال مهاجرت‌ها و اجرای سرور:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 6. ساخت کاربر ادمین:
```bash
python manage.py createsuperuser
```

---

## 🐳 اجرای Docker (اختیاری)

```bash
docker build -t divine-beauty .
docker run -p 8000:8000 divine-beauty
```

---

## 📁 ساختار پروژه

```
DivineBeauty/
├── A/                      # تنظیمات پروژه Django
├── accounts/               # مدیریت کاربران و احراز هویت
├── home/                   # صفحات عمومی: خانه، درباره ما، جستجو
├── products/               # مدیریت محصولات و کامنت‌ها
├── products_api/           # API برای محصولات
├── order/                  # سبد خرید و سفارشات
├── templates/              # قالب‌های HTML
├── static/                 # فایل‌های استاتیک
├── Dockerfile              # تعریف تصویر Docker
├── requirements.txt        # وابستگی‌های پایتون
├── manage.py
```

---

## 📧 ارتباط با من

[GitHub Profile](https://github.com/Sajjadhosseinrezaei)

---

