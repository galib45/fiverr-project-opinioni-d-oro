const editor = document.getElementById('editor')
const toolbarOptions = [
  ['bold', 'italic', 'underline'], ['blockquote', 'code-block'],        // toggled buttons
  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'align': [] }],
  ['clean']                                         // remove formatting button
];
let quill = new Quill(editor, {
  modules: {
    toolbar: toolbarOptions
  },
  placeholder: 'Write the article ...',
  theme: 'snow'
});

toolbar = document.querySelector('.ql-toolbar');
editor.style.borderWidth = '2px';
editor.style.maxHeight = '400px';
editor.style.overflowY = 'scroll';
toolbar.style.borderWidth = '2px';
validationError = false;

// Get all the elements
const titleErrorEl = document.getElementById("title-error");
const contentErrorEl = document.getElementById("content-error");

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
    input: document.getElementById("title"),
    errorElement: titleErrorEl,
    message: "Title of the article is required.",
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

quill.on('text-change', ()=>{
  document.getElementById('content').value = editor.querySelector('.ql-editor').innerHTML;
  if (editor.querySelector('.ql-editor').textContent === '') {
    editor.style.borderColor = '#f44336';
    toolbar.style.borderColor = '#f44336';
    contentErrorEl.textContent = 'Content of the Article is required.';
  } else {
    editor.style.borderColor = '#2196f3';
    toolbar.style.borderColor = '#2196f3';
    contentErrorEl.textContent = '';
  }
});

const form = document.getElementById("addarticle-form")
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
  if (editor.querySelector('.ql-editor').textContent === '') {
    editor.style.borderColor = '#f44336';
    toolbar.style.borderColor = '#f44336';
    contentErrorEl.textContent = 'Content of the Article is required.';
    event.preventDefault();
  } else {
    editor.style.borderColor = '';
    toolbar.style.borderColor = '';
    contentErrorEl.textContent = '';
  }
 
});
