    document.addEventListener('DOMContentLoaded', function() {
    const thumbnails = document.querySelectorAll('.gallery-thumb');
    const mainImage = document.getElementById('main-image');
    
        thumbnails.forEach(function(thumb) {
            thumb.addEventListener('click', function() {
                const newImageSrc = this.getAttribute('data-src');
                mainImage.setAttribute('src', newImageSrc);
            });
        });
    });
    document.addEventListener('DOMContentLoaded', function() {
        const decreaseBtn = document.getElementById('decrease-btn');
        const increaseBtn = document.getElementById('increase-btn');
        const quantityInput = document.getElementById('quantity-number');
    
        // افزایش مقدار
        increaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
        });
    
        // کاهش مقدار
        decreaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });
    });
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.reply-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                // همه فرم‌های ریپلای را مخفی کن
                document.querySelectorAll('.reply-form').forEach(f => f.classList.add('d-none'));
                // فرم مربوط به این کامنت را نمایش بده
                const parentId = btn.getAttribute('data-parent');
                document.querySelector('.reply-form[data-parent="' + parentId + '"]').classList.remove('d-none');
            });
        });
        document.querySelectorAll('.cancel-reply').forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                btn.closest('.reply-form').classList.add('d-none');
            });
        });
    });
