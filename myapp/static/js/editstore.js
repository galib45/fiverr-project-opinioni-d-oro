const generateIdButton = document.getElementById("generate-id-button");
const googleMapURLElement = document.getElementById("google_map_url");
const placeIdElement = document.getElementById("place_id");
const hexIdElement = document.getElementById("hex_id");
const saveExtraButton = document.getElementById("save-extra");
const accountState = document.getElementById("account_state");
const package = document.getElementById("package");

const generateIdLoader = generateIdButton.parentElement.querySelector('.loader'); 
const saveExtraLoader = saveExtraButton.parentElement.querySelector('.loader'); 

saveExtraButton.onclick = (event) => {
  saveExtraLoader.classList.remove('hidden'); 
  
  fetch(window.location.href + '/extras', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      state: accountState.value,
      package: package.value
    })
  }).then(resp => resp.json()).then(
      (json) => {
        if (json.status == 'success'){
          saveExtraLoader.classList.add('hidden');
        }      
      }
    );
}; 

validationError = false;

// Get all the elements
const nameErrorEl = document.getElementById("name-error");
const phoneNumberErrorEl = document.getElementById("phone-number-error");
const addressErrorEl = document.getElementById("address-error");
const googleMapURLErrorEl = document.getElementById("google-map-url-error");
const placeIdErrorEl = document.getElementById("place-id-error");
const hexIdErrorEl = document.getElementById("hex-id-error");


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
const googleMapLinkRegex = /^https:\/\/maps\.app\.goo\.gl\/[A-Za-z0-9_-]+/;


// Define an array of objects with input elements, corresponding error elements, messages, and regex for password validation
const inputs = [{
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
  inputElement.addEventListener("input", () => {
    validateInput(
      inputElement.value.trim(),
      inputObj.errorElement,
      inputObj.message,
      inputObj.regex,
      inputElement,
    );
  });
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
  generateIdLoader.classList.remove('hidden');
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
      generateIdLoader.classList.add('hidden');
    });
});

const form = document.getElementById("editstore-form")
form.addEventListener("submit", function(event) {
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
