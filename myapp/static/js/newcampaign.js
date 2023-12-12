textAreas = document.querySelectorAll('textarea');
textAreas.forEach((textArea) => {
  textArea.oninput = (event) => {
    textArea.style.height = 'auto';
    textArea.style.height = textArea.scrollHeight + 'px';
  };
});

new AirDatepicker('#expire_date', {
  isMobile: true,
  autoClose: true,
  dateFormat: 'MMMM dd, yyyy',
  locale: {
    days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
    months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    today: 'Today',
    clear: 'Clear',
    dateFormat: 'MM/dd/yyyy',
    timeFormat: 'hh:mm aa',
    firstDay: 0
  }
});

validationError = false;

// Get all the elements
const nameErrorEl = document.getElementById("name-error");
const descriptionErrorEl = document.getElementById("description-error")
const offerErrorEl = document.getElementById("offer-error")
const expireDateErrorEl = document.getElementById("expire-date-error")

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

// Define an array of objects with input elements, corresponding error elements, messages, and regex for password validation
const inputs = [{
  input: document.getElementById("name"),
  errorElement: nameErrorEl,
  message: "Name of the campaign is required.",
}, {
  input: document.getElementById("description"),
  errorElement: descriptionErrorEl,
  message: "Short Description is required.",
}, {
  input: document.getElementById("offer"),
  errorElement: offerErrorEl,
  message: "Campaign offer is required.",
}, {
  input: document.getElementById("expire_date"),
  errorElement: expireDateErrorEl,
  message: "Expire Date is required.",
}];

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

document.getElementById("newcampaign-form").addEventListener("submit", function(event) {
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
