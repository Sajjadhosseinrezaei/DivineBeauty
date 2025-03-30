// sm(mobile) now
/*const smNav = document.querySelector('.snav');
const closeBtn = document.querySelector('.snav__close-btn');
const closeBtnIcn = document.querySelector('.snav__close-btn-icon');

const navOpenedClass = 'right-0';
const navClosedClass = '-right-[300px]';
const arrowRightClass = 'ri-menu-4-line';
const arrowLeftClass = 'ri-close-large-line';

closeBtn.addEventListener('click', () => {
    if (smNav.classList.contains(navClosedClass)) {
        smNav.classList.toggle(navOpenedClass);

        closeBtnIcn.classList.toggle(arrowRightClass);
        closeBtnIcn.classList.toggle(arrowLeftClass);
    }
})*/

const smNav = document.querySelector('.snav');
const closeBtn = document.querySelector('.snav__close-btn');
const closeBtnIcn = document.querySelector('.snav__close-btn-icon');

const navOpenedClass = 'right-0';
const navClosedClass = '-right-[300px]';
const arrowRightClass = 'ri-menu-4-line';
const arrowLeftClass = 'ri-close-large-line';

closeBtn.addEventListener('click', () => {
    if (smNav.classList.contains(navClosedClass)) {
        smNav.classList.remove(navClosedClass);
        smNav.classList.add(navOpenedClass);
    } else {
        smNav.classList.remove(navOpenedClass);
        smNav.classList.add(navClosedClass);
    }

    closeBtnIcn.classList.toggle(arrowRightClass);
    closeBtnIcn.classList.toggle(arrowLeftClass);
});

