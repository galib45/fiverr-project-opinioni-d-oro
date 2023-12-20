const navbar = document.getElementById('dashboard-navbar');
const overlay = document.getElementById('dashboard-overlay');
const navmenu = document.getElementById('dashboard-navmenu');

navmenu.onclick = () => {
  console.log('navmenu click');
  navbar.classList.remove('hidden');
  overlay.classList.remove('hidden');
  const qlContainer = document.querySelector('.ql-container');
  if (qlContainer) qlContainer.style.position = 'unset';
};
overlay.onclick = () => {
  console.log('overlay click');
  navbar.classList.add('hidden');
  overlay.classList.add('hidden');
  const qlContainer = document.querySelector('.ql-container');
  if (qlContainer) qlContainer.style.position = 'relative';
};


// datetime utc to cet 
document.querySelectorAll('span.datetime').forEach((span)=> {
  span.innerHTML = moment(span.textContent).add(1, 'hours').format('MMMM DD, YYYY hh:mm:ss A') + ' CET';
});
