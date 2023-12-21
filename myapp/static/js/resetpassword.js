validationError = false;

// Get all the elements
const passwordErrorEl = document.getElementById("password-error");
const confirmPasswordErrorEl = document.getElementById("confirm-password-error");

// Get the password and confirm password input elements
const passwordElement = document.getElementById("password");
const confirmPasswordElement = document.getElementById("confirm_password");

function validateInput(inputValue, errorElement, errorMessage, regex, inputElement) {
  if (inputValue === "") {
    validationError = true;
    errorElement.textContent = errorMessage;
    errorElement.style.display = "block";
    inputElement.classList.remove("valid-input");
    inputElement.classList.add("invalid-input");
  } else if (regex && !regex.test(inputValue)) {
    validationError = true;
    errorElement.textContent = "Invalid format";
    if (inputElement == passwordElement)
      errorElement.textContent = "minimum 6 characters, at least one number";
    errorElement.style.display = "block";
    inputElement.classList.remove("valid-input");
    inputElement.classList.add("invalid-input");
  } else {
    errorElement.textContent = "";
    errorElement.style.display = "none";
    inputElement.classList.remove("invalid-input");
    inputElement.classList.add("valid-input");
  }
}

const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/; // Password format: 6-10 characters, at least one number

confirmPasswordElement.addEventListener("input", () => {
  // Check if the passwords match
  if (passwordElement.value !== confirmPasswordElement.value) {
    validationError = true;
    confirmPasswordErrorEl.textContent = "Passwords do not match";
    confirmPasswordErrorEl.style.display = "block";
    confirmPasswordElement.classList.remove("valid-input");
    confirmPasswordElement.classList.add("invalid-input");
  } else {
    confirmPasswordErrorEl.textContent = "";
    confirmPasswordErrorEl.style.display = "none";
    confirmPasswordElement.classList.remove("invalid-input");
    confirmPasswordElement.classList.add("valid-input");
  }
});

// Define an array of objects with input elements, corresponding error elements, messages, and regex for password validation
const inputs = [
  {
    input: passwordElement,
    errorElement: passwordErrorEl,
    message: "Password is required.",
    regex: passwordRegex,
  },
  {
    input: confirmPasswordElement,
    errorElement: confirmPasswordErrorEl,
    message: "Please confirm the password.",
  },
];

// Attach input event listeners to each input element
inputs.forEach((inputObj) => {
  const inputElement = inputObj.input;
  if (inputElement != confirmPasswordElement) {
    inputElement.addEventListener("input", () => {
      validateInput(
        inputElement.value.trim(),
        inputObj.errorElement,
        inputObj.message,
        inputObj.regex,
        inputElement,
      );
    });
  }
});


document
  .getElementById("resetpass-form")
  .addEventListener("submit", function (event) {
    // Check if the password and confirm password match
    if (passwordElement.value !== confirmPasswordElement.value) {
      validationError = true;
      confirmPasswordErrorEl.textContent = "Passwords do not match";
      confirmPasswordErrorEl.style.display = "block";
      confirmPasswordElement.classList.remove("valid-input");
      confirmPasswordElement.classList.add("invalid-input");
    }

    // Revalidate all inputs
    validationError = false;
    inputs.forEach((inputObj) => {
      const inputElement = inputObj.input;
      validateInput(
        inputElement.value,
        inputObj.errorElement,
        inputObj.message,
        inputObj.regex,
        inputElement,
      );
    });

    if (validationError) event.preventDefault();
  });
