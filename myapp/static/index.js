navbarMenuEl = document.querySelector('.navbar-menu');
navbarVerticalEl = document.querySelector('.navbar-vertical');

navbarMenuEl.addEventListener('click', function() {
    console.log(navbarVerticalEl.style.height);
    if (navbarVerticalEl.style.height != '270px') navbarVerticalEl.style.height = '270px';
    else navbarVerticalEl.style.height = '0px';
});
