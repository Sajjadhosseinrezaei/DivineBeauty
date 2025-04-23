document.addEventListener('DOMContentLoaded', function() {
    // نوار ناوبری چسبنده
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // انیمیشن اسکرول به بخش‌ها
    const smoothScroll = function(target, duration) {
        const targetElement = document.querySelector(target);
        const targetPosition = targetElement.offsetTop - 80;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;

        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }

        requestAnimationFrame(animation);
    };

    // اضافه کردن محصول به سبد خرید
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('h3').textContent;
            const productPrice = productCard.querySelector('.price').textContent;
            
            // نمایش پیام اضافه شدن به سبد خرید
            showNotification(`${productName} به سبد خرید اضافه شد`);
            
            // افزایش شمارنده سبد خرید
            updateCartCounter();
        });
    });

    // نمایش پیام (نوتیفیکیشن)
    function showNotification(message) {
        // ایجاد عنصر نوتیفیکیشن
        const notification = document.createElement('div');
        notification.classList.add('notification');
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-check-circle"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // نمایش نوتیفیکیشن با انیمیشن
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // حذف نوتیفیکیشن بعد از ۳ ثانیه
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // بروزرسانی شمارنده سبد خرید
    function updateCartCounter() {
        const cartCounter = document.querySelector('.cart-counter');
        let currentCount = parseInt(cartCounter.textContent);
        cartCounter.textContent = currentCount + 1;
        
        // انیمیشن شمارنده
        cartCounter.classList.add('pulse');
        setTimeout(() => {
            cartCounter.classList.remove('pulse');
        }, 300);
    }

    // اعمال استایل به نوتیفیکیشن با CSS داینامیک
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            left: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            padding: 15px 20px;
            z-index: 1000;
            transform: translateY(-100px);
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .notification.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        .notification-content {
            display: flex;
            align-items: center;
        }
        
        .notification-content i {
            color: #4CAF50;
            font-size: 20px;
            margin-left: 10px;
        }
        
        .pulse {
            animation: pulse-animation 0.3s;
        }
        
        @keyframes pulse-animation {
            0% { transform: scale(1); }
            50% { transform: scale(1.5); }
            100% { transform: scale(1); }
        }
        
        .navbar-scrolled {
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            background-color: #fff !important;
        }
    `;
    document.head.appendChild(style);
});

// فعال‌سازی زیرمنوها در حالت هاور و کلیک
document.addEventListener('DOMContentLoaded', function () {
    const submenus = document.querySelectorAll('.dropdown-submenu');

    submenus.forEach(function (submenu) {
        const trigger = submenu.querySelector('.dropdown-toggle');

        // زیرمنو را در هاور فعال کن
        trigger.addEventListener('mouseenter', function () {
            closeAllSubmenus(submenu);
            const dropdown = submenu.querySelector('.dropdown-menu');
            if (dropdown) dropdown.style.display = 'block';
        });

        // زیرمنو را در هاور غیرفعال کن
        submenu.addEventListener('mouseleave', function () {
            const dropdown = submenu.querySelector('.dropdown-menu');
            if (dropdown) dropdown.style.display = 'none';
        });

        // کلیک روی لینک ها برای رفتن به URL
        trigger.addEventListener('click', function (e) {
            if (!submenu.querySelector('.dropdown-menu').classList.contains('show')) {
                // این بخش از کد که باعث نمایش زیرمنو می‌شود
                submenu.querySelector('.dropdown-menu').classList.toggle('show');
            }
            // اینجا هیچگونه جلوگیری از انتقال به URL انجام نمی‌دهیم
        });
    });

    function closeAllSubmenus(current) {
        document.querySelectorAll('.dropdown-submenu .dropdown-menu').forEach(menu => {
            if (!current.contains(menu)) {
                menu.style.display = 'none';
            }
        });
    }
});

// موبایل - کلیک برای باز کردن زیرمنو
document.addEventListener('DOMContentLoaded', function () {
    if (window.innerWidth <= 992) {
        document.querySelectorAll('.dropdown-submenu > .dropdown-toggle').forEach(function (el) {
            el.addEventListener('click', function (e) {
                e.preventDefault(); // جلوگیری از حرکت به لینک فقط زمانی که زیرمنو باز است
                const parent = this.parentElement;
                parent.classList.toggle('show');
            });
        });
    }
});
