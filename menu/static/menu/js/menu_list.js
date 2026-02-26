(function () {
    'use strict';

    var ROOT_CLASS = 'menu-list--scroll-root';
    var ITEM_CLASS = 'food-row';
    var VISIBLE_CLASS = 'food-row--in-view';
    var MODAL_ID = 'food-modal';
    var MODAL_BODY_ID = 'food-modal__body';
    var API_FOODS = '/api/foods/';

    function formatPrice(value) {
        return '€' + Number(value).toFixed(2);
    }

    function formatDiscount(discount) {
        if (discount && discount > 0) {
            return '-' + discount + '%';
        }
        return '';
    }

    function buildModalContent(data) {
        var imageUrl = data.header_image || null;
        var imgHtml = '';
        if (imageUrl) {
            imgHtml = '<div class="food-modal__image-wrap">' +
                '<img src="' + escapeHtml(imageUrl) + '" alt="" class="food-modal__image">' +
                '</div>';
        }
        var badges = [];
        if (data.discount && data.discount > 0) {
            badges.push('<span class="food-modal__badge food-modal__badge--discount">' + escapeHtml(formatDiscount(data.discount)) + ' OFF</span>');
        }
        var badgesHtml = badges.length ? '<div class="food-modal__badges">' + badges.join('') + '</div>' : '';
        var descHtml = data.description
            ? '<div class="food-modal__description">' + escapeHtml(data.description) + '</div>'
            : '';
        var priceHtml = '<div class="food-modal__price">';
        if (data.discount && data.discount > 0) {
            priceHtml += '<span class="food-modal__price-original">' + escapeHtml(formatPrice(data.price)) + '</span>';
        }
        priceHtml += '<span>' + escapeHtml(formatPrice(data.final_price)) + '</span></div>';
        var toppingsHtml = '';
        if (data.toppings && data.toppings.length > 0) {
            var items = data.toppings.map(function (t) {
                var top = t.topping;
                var name = escapeHtml(top.name);
                var price = formatPrice(top.final_price);
                var desc = top.description ? '<br><span class="food-modal__topping-desc">' + escapeHtml(top.description) + '</span>' : '';
                return '<li class="food-modal__topping">' +
                    '<span class="food-modal__topping-name">' + name + '</span>' + desc + ' &mdash; ' + price +
                    '</li>';
            });
            toppingsHtml = '<h3 class="food-modal__toppings-title">Available Toppings</h3>' +
                '<ul class="food-modal__toppings-list">' + items.join('') + '</ul>';
        }
        return imgHtml +
            '<h2 id="food-modal-title" class="food-modal__title">' + escapeHtml(data.name) + '</h2>' +
            badgesHtml +
            descHtml +
            priceHtml +
            toppingsHtml;
    }

    function escapeHtml(text) {
        if (text == null) return '';
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function getModal() {
        return document.getElementById(MODAL_ID);
    }

    function getModalBody() {
        return document.getElementById(MODAL_BODY_ID);
    }

    function openModal() {
        var modal = getModal();
        if (modal) {
            modal.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal() {
        var modal = getModal();
        if (modal) {
            modal.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    }

    function showFoodInModal(foodId) {
        var body = getModalBody();
        if (!body) return;
        body.innerHTML = '<div class="food-modal__loading">Loading…</div>';
        openModal();
        fetch(API_FOODS + foodId + '/')
            .then(function (res) {
                if (!res.ok) throw new Error('Not found');
                return res.json();
            })
            .then(function (data) {
                body.innerHTML = buildModalContent(data);
            })
            .catch(function () {
                body.innerHTML = '<div class="food-modal__error">Could not load details.</div>';
            });
    }

    function bindModal() {
        var modal = getModal();
        if (!modal) return;
        var backdrop = modal.querySelector('.food-modal__backdrop');
        var closeBtn = modal.querySelector('.food-modal__close');
        if (backdrop) backdrop.addEventListener('click', closeModal);
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
                closeModal();
            }
        });
    }

    function bindFoodRowClicks() {
        var root = document.querySelector('.' + ROOT_CLASS);
        if (!root) return;
        root.addEventListener('click', function (e) {
            var link = e.target.closest('.food-row__link');
            if (!link) return;
            var id = link.getAttribute('data-food-id');
            if (id) {
                e.preventDefault();
                showFoodInModal(id);
            }
        });
    }

    function observeFoodRows() {
        var root = document.querySelector('.' + ROOT_CLASS);
        if (!root) return;
        var items = root.querySelectorAll('.' + ITEM_CLASS);
        if (!items.length) return;
        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add(VISIBLE_CLASS);
                    } else {
                        entry.target.classList.remove(VISIBLE_CLASS);
                    }
                });
            },
            {
                root: null,
                rootMargin: '-8% 0px -8% 0px',
                threshold: 0.2
            }
        );
        items.forEach(function (el) { observer.observe(el); });
    }

    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', run);
        } else {
            run();
        }
    }

    function run() {
        observeFoodRows();
        bindModal();
        bindFoodRowClicks();
    }

    init();
})();
