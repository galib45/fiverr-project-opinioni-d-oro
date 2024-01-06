const navbar = document.getElementById('dashboard-navbar');
const overlay = document.getElementById('dashboard-overlay');
const navmenu = document.getElementById('dashboard-navmenu');
const modalRoot = document.getElementById('modal-root');
const modalBackdrop = document.getElementById('modal-backdrop');
const modalPanel = document.getElementById('modal-panel');
const modalLeaveButton = document.getElementById('modal-leave');
const modalAcceptButton = document.getElementById('modal-accept');

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

function showModal() {
  modalRoot.classList.remove('hidden');
  setTimeout(() => {
    modalBackdrop.classList.add('opacity-100', 'ease-out', 'duration-300');
    modalPanel.classList.add('pointer-events-auto', 'select-auto', 'opacity-100', 'translate-y-0', 'sm:scale-100', 'ease-out', 'duration-300');
  }, 10);
}

function hideModal() {
  modalBackdrop.classList.remove('opacity-100', 'ease-out', 'duration-300');
  modalBackdrop.classList.add('opacity-0', 'ease-in', 'duration-200');
  modalPanel.classList.remove('pointer-events-auto', 'select-auto', 'opacity-100', 'translate-y-0', 'sm:scale-100', 'ease-out', 'duration-300');
  modalPanel.classList.add('pointer-events-none', 'select-none', 'opacity-0', 'translate-y-4', 'sm:translate-y-0', 'sm:scale-95', 'ease-in', 'duration-200');
  setTimeout(() => {
    modalRoot.classList.add('hidden');
  }, 200);
}

modalLeaveButton.onclick = () => {
  location.assign('/logout');
}

modalAcceptButton.onclick = () => {
  fetch('/accept_policies')
  .then(resp => resp.text())
  .then((text) => {
    if(text === 'True') hideModal();
  });
}

if(policies_accepted !== 'True') showModal();
  
// datetime utc to cet 
document.querySelectorAll('span.datetime').forEach((span)=> {
  span.innerHTML = moment(span.textContent).add(1, 'hours').format('MMMM DD, YYYY hh:mm:ss A') + ' CET';
});
