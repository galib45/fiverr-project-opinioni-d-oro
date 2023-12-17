const navbar = document.getElementById('dashboard-navbar');
const overlay = document.getElementById('dashboard-overlay');
const navmenu = document.getElementById('dashboard-navmenu');
navmenu.onclick = () => {
  console.log('navmenu click');
  navbar.classList.remove('hidden');
  overlay.classList.remove('hidden');
};
overlay.onclick = () => {
  console.log('overlay click');
  navbar.classList.add('hidden');
  overlay.classList.add('hidden');
};
