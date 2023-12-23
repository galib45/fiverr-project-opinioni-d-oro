const form = document.querySelector('form');
const email = document.getElementById('email');
const generalCouponOffer = document.getElementById('general_coupon_offer');
const initialValues = {};
initialValues.email = email.value.trim();
initialValues.general_coupon_offer = generalCouponOffer.value.trim();
let formchanged = false;
let submitting = false;

const messagesContainer = document.createElement('div');
const main = document.getElementById('main');
main.prepend(messagesContainer);

form.querySelectorAll('input').forEach((input) => {
  input.oninput = () => {  
    formchanged = true; 
  };
});

form.onsubmit = (event) => {
  if (email.value.trim() === initialValues.email 
    && generalCouponOffer.value.trim() === initialValues.general_coupon_offer) { 
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
  if(formchanged && !submitting) {
    event.preventDefault();
    return 'Your changes will not be saved!';
  }
};
