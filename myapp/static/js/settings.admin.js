const form = document.querySelector('form');
const email = document.getElementById('email');
const initialvalue = email.value.trim();
let formchanged = false;
let submitting = false;

const messagesContainer = document.createElement('div');
const main = document.getElementById('main');
main.prepend(messagesContainer);

form.onchange = () => { formchanged = true; };

form.onsubmit = (event) => {
  if (email.value.trim() === initialvalue) { 
    event.preventDefault();
    messageElem = document.createElement('div')
    messageElem.innerText = 'Nothing to save';
    messageElem.classList.add('alert-info');
    messagesContainer.appendChild(messageElem);
    setTimeout(() => {
      messagesContainer.innerHTML = '';
    }, 3000);
  }
  submitting = true;
}

onbeforeunload = (event) => {
  if(formchanged && !submitting) event.preventDefault();
};
