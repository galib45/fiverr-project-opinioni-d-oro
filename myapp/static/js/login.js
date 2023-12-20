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

function validateInput(inputValue, errorElement, errorMessage, regex, inputElement) {
  if (inputValue === '') {
    validationError = true;
    errorElement.textContent = errorMessage;
    errorElement.style.display = 'block';
    inputElement.classList.remove('valid-input');
    inputElement.classList.add('invalid-input');
  } else if (regex && !regex.test(inputValue)) {
    validationError = true;
    errorElement.textContent = 'Invalid format';
    errorElement.style.display = 'block';
    inputElement.classList.remove('valid-input');
    inputElement.classList.add('invalid-input');
  } else {
    errorElement.textContent = '';
    errorElement.style.display = 'none';
    inputElement.classList.remove('invalid-input');
    inputElement.classList.add('valid-input');
  }
}
// Get all the elements
const usernameErrorEl = document.getElementById('username-error');
const passwordErrorEl = document.getElementById('password-error');
// Define an array of objects with input elements, corresponding error elements, messages, and regex for password validation
const inputs = [{
    input: document.getElementById('username'),
    errorElement: usernameErrorEl,
    message: 'Username is required.'
  },
  {
    input: document.getElementById('password'),
    errorElement: passwordErrorEl,
    message: 'Password is required.'
  }
];
// Attach input event listeners to each input element
inputs.forEach((inputObj) => {
  const inputElement = inputObj.input;
  inputElement.addEventListener('input', () => {
    validateInput(inputElement.value.trim(), inputObj.errorElement, inputObj.message, inputObj.regex, inputElement);
  });
});
document.getElementById('login-form').addEventListener('submit', function(event) {
    // Revalidate all inputs
  validationError = false;
  inputs.forEach((inputObj) => {
    const inputElement = inputObj.input;
    validateInput(inputElement.value.trim(), inputObj.errorElement, inputObj.message, inputObj.regex, inputElement);
  });
  if (validationError) event.preventDefault();
});
