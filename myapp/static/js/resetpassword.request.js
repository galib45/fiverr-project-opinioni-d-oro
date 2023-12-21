validationError = false;

// Get all the elements
const emailErrorEl = document.getElementById("email-error");
const emailElement = document.getElementById("email");

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
    if (regex == usernameRegex)
      errorElement.textContent = "no spaces, 3-15 characters, must start with a letter";
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

const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;


// Define an array of objects with input elements, corresponding error elements, messages, and regex for password validation
const inputs = [
  {
    input: document.getElementById("email"),
    errorElement: emailErrorEl,
    message: "Email is required.",
    regex: emailRegex,
  }
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
  .getElementById("resetpassreq-form")
  .addEventListener("submit", function (event) {
    
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
