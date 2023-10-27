navbarMenuEl = document.querySelector('.navbar-menu');
navbarWrapperEl = document.querySelector('.navbar-wrapper');

navbarMenuEl.addEventListener('click', function() {
    console.log(navbarWrapperEl.style.gridTemplateRows);
    if (navbarWrapperEl.style.gridTemplateRows !== '1fr') navbarWrapperEl.style.gridTemplateRows = '1fr';
    else navbarWrapperEl.style.gridTemplateRows = '0fr';
});
