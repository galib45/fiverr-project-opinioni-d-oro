document.addEventListener("DOMContentLoaded", () => {
  // animate navbar menu
  const navbarWapperEl = document.querySelector(".navbar-wrapper");
  const navbarVerticalEl = document.querySelector(".navbar-vertical");

  document.getElementById("navbar-menu").onclick = () => {
    if (navbarWapperEl.style.gridTemplateRows !== "1fr") {
      navbarWapperEl.style.gridTemplateRows = "1fr";
      navbarVerticalEl.style.paddingBottom = "1.25rem";
    } else {
      navbarWapperEl.style.gridTemplateRows = "0fr";
      navbarVerticalEl.style.paddingBottom = "0";
    }
  };
  
  // password visibility toggle
  document.querySelectorAll('.password-input-container > span').forEach((icon) => {
    icon.addEventListener('click', (event) => {
      toggleElement = event.target;
      parentDiv = toggleElement.closest('div');
      inputElement = parentDiv.querySelector('input');
      if (inputElement.type === 'password') inputElement.type = 'text';
      else inputElement.type = 'password';
      parentDiv.querySelectorAll('span').forEach((span) => {
        span.classList.toggle('hidden');
      });
    });
  });

  // datetime utc to cet 
  document.querySelectorAll('span.datetime').forEach((span)=> {
    span.innerHTML = moment(span.textContent).add(1, 'hours').format('MMMM DD, YYYY hh:mm:ss A') + ' CET';
  });
});
