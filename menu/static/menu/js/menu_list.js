/* global modal controller – functions are called directly from onclick attributes in the template */
var menuModal = {

    open: function (foodId) {
        var bodies = document.querySelectorAll('.food-modal__body-inner');
        for (var i = 0; i < bodies.length; i++) {
            bodies[i].style.display = 'none';
        }
        var target = document.getElementById('food-modal-body-' + foodId);
        if (target) target.style.display = 'block';
        var modal = document.getElementById('food-modal');
        if (modal) modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    },

    close: function () {
        var modal = document.getElementById('food-modal');
        if (modal) modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    },

    prev: function (btn) {
        var body = btn.closest('.food-modal__body-inner');
        var wrap = body.querySelector('.food-modal__banner-wrap');
        var idx  = parseInt(wrap.getAttribute('data-current-index') || '0', 10);
        menuModal._slide(body, idx - 1);
    },

    next: function (btn) {
        var body = btn.closest('.food-modal__body-inner');
        var wrap = body.querySelector('.food-modal__banner-wrap');
        var idx  = parseInt(wrap.getAttribute('data-current-index') || '0', 10);
        menuModal._slide(body, idx + 1);
    },

    thumb: function (btn, index) {
        menuModal._slide(btn.closest('.food-modal__body-inner'), index);
    },

    _slide: function (body, index) {
        var slides = body.querySelectorAll('.food-modal__slide');
        var thumbs = body.querySelectorAll('.food-modal__thumb');
        var wrap   = body.querySelector('.food-modal__banner-wrap');
        var n      = slides.length;
        if (!n) return;
        index = (index % n + n) % n;
        for (var i = 0; i < slides.length; i++) {
            slides[i].style.display = i === index ? 'block' : 'none';
        }
        for (var j = 0; j < thumbs.length; j++) {
            thumbs[j].classList.toggle('food-modal__thumb--active', j === index);
        }
        if (wrap) wrap.setAttribute('data-current-index', String(index));
    }
};

/* close on Escape */
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') menuModal.close();
});

/* scroll zoom via IntersectionObserver */
document.addEventListener('DOMContentLoaded', function () {
    if (!window.IntersectionObserver) return;
    var items = document.querySelectorAll('.food-row');
    if (!items.length) return;
    var observer = new IntersectionObserver(function (entries) {
        for (var i = 0; i < entries.length; i++) {
            entries[i].target.classList.toggle('food-row--in-view', entries[i].isIntersecting);
        }
    }, { rootMargin: '-8% 0px -8% 0px', threshold: 0.2 });
    for (var i = 0; i < items.length; i++) {
        observer.observe(items[i]);
    }
});
