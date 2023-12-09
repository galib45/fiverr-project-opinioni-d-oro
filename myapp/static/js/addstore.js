const generateIdButton = document.getElementById("generate-id-button");
const googleMapURLElement = document.getElementById("google_map_url");
const placeIdElement = document.getElementById("place_id");
const hexIdElement = document.getElementById("hex_id");
const loaderElement = document.querySelector(".loader");

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

validationError = false;

// Get all the elements
const usernameErrorEl = document.getElementById("username-error");
const emailErrorEl = document.getElementById("email-error");
const passwordErrorEl = document.getElementById("password-error");
const confirmPasswordErrorEl = document.getElementById(
  "confirm-password-error",
);
const nameErrorEl = document.getElementById("name-error");
const phoneNumberErrorEl = document.getElementById("phone-number-error");
const addressErrorEl = document.getElementById("address-error");
const googleMapURLErrorEl = document.getElementById("google-map-url-error");
const placeIdErrorEl = document.getElementById("place-id-error");
const hexIdErrorEl = document.getElementById("hex-id-error");

// Get the password and confirm password input elements
const passwordElement = document.getElementById("password");
const confirmPasswordElement = document.getElementById("confirm_password");

function validateInput(
  inputValue,
  errorElement,
  errorMessage,
  regex,
  inputElement,
) {
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
    if (regex == usernameRegex)
      errorElement.textContent =
        "no spaces, 3-15 characters, must start with a letter";
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

// Define regular expressions for email and Google Map link validation
const usernameRegex = /^[a-zA-Z0-9_-]{3,15}$/;
const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const googleMapLinkRegex = /^https:\/\/maps\.app\.goo\.gl\/[A-Za-z0-9_-]+/;
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
    input: document.getElementById("username"),
    errorElement: usernameErrorEl,
    message: "Username is required.",
    regex: usernameRegex,
  },
  {
    input: document.getElementById("email"),
    errorElement: emailErrorEl,
    message: "Email is required.",
    regex: emailRegex,
  },
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
  {
    input: document.getElementById("name"),
    errorElement: nameErrorEl,
    message: "Name of the store is required.",
  },
  {
    input: document.getElementById("phone_number"),
    errorElement: phoneNumberErrorEl,
    message: "Phone number of the store owner is required.",
  },
  {
    input: document.getElementById("address"),
    errorElement: addressErrorEl,
    message: "Store address is required.",
  },
  {
    input: googleMapURLElement,
    errorElement: googleMapURLErrorEl,
    message: "Google Map Link of the store is required.",
    regex: googleMapLinkRegex,
  },
  {
    input: placeIdElement,
    errorElement: placeIdErrorEl,
    message: "Place ID is required.",
  },
  {
    input: hexIdElement,
    errorElement: hexIdErrorEl,
    message: "Hex ID is required.",
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

generateIdButton.addEventListener("click", (event) => {
  placeIdErrorEl.style.display = "none";
  hexIdErrorEl.style.display = "none";
  placeIdElement.value = "";
  hexIdElement.value = "";
  validationError = false;

  validateInput(
    googleMapURLElement.value.trim(),
    googleMapURLErrorEl,
    "Google Map Link of the store is required.",
    googleMapLinkRegex,
    googleMapURLElement,
  );
  if (validationError) return;
  loaderElement.style.display = "block";
  console.log("generating id ...");
  url = "/getid/" + googleMapURLElement.value.trim().split("/").pop();
  console.log(url);
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.place_id == null) {
        placeIdErrorEl.innerHTML =
          'Could not get place id. Retry or Visit this <a href="https://developers.google.com/maps/documentation/places/web-service/place-id#find-id" target="_blank">link</a> to get the place id.';
        placeIdErrorEl.style.display = "block";
      } else {
        placeIdElement.value = data.place_id;
        placeIdErrorEl.innerHTML = "";
        placeIdErrorEl.style.display = "none";
      }
      if (data.hex_id == null) {
        hexIdErrorEl.textContent = "Could not get hex id. Please retry.";
        hexIdErrorEl.style.display = "block";
      } else {
        hexIdElement.value = data.hex_id;
        hexIdErrorEl.textContent = "";
        hexIdErrorEl.style.display = "none";
      }
      loaderElement.style.display = "none";
    });
});

document
  .getElementById("addstore-form")
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
