document.addEventListener("DOMContentLoaded", () => {
  // hover effect for icons in navbar menu items
  icons = document.querySelectorAll(".navbar-wrapper svg");
  icons.forEach((icon) => {
    parent = icon.closest("div");
    parent.onmouseover = () => {
      icon.classList.add("fill-teal-900");
    };
    parent.onmouseleave = () => {
      icon.classList.remove("fill-teal-900");
    };
  });
  
  // animate navbar menu
  const navbarWapperEl = document.querySelector('.navbar-wrapper');
  const navbarVerticalEl = document.querySelector('.navbar-vertical');
  
  document.getElementById('navbar-menu').onclick = () => {
    if(navbarWapperEl.style.gridTemplateRows !== '1fr') {
      navbarWapperEl.style.gridTemplateRows = '1fr';
      navbarVerticalEl.style.paddingBottom = '1.25rem';
    }
    else {
      navbarWapperEl.style.gridTemplateRows = '0fr';
      navbarVerticalEl.style.paddingBottom = '0';
    }
  };

  // hover effect for icons in buttons
  icons = document.querySelectorAll('.button svg, input[type="submit"] svg');
  icons.forEach((icon) => {
    parent = icon.closest('div');
    parent.onmouseover = () => {
      icon.classList.add('fill-white');
    };
    parent.onmouseleave = () => {
      icon.classList.remove('fill-white');
    }
  });
});
