const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');

const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');

function showError(input, value) {
  input.innerHTML = value;
  input.classList.replace('mt-0', 'mt-2');
}

function removeError(input) {
  input.innerHTML = '';
  input.classList.replace('mt-2', 'mt-0');
}

function validateEmail(input) {
  const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  return input.value.match(validRegex);
}

// eslint-disable-next-line no-unused-vars
function validatePassword(input) {
  return true;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  if (!validateEmail(email)) {
    showError(emailError, 'กรุณาป้อนอีเมลให้ถูกต้อง.');
    return;
  }

  if (!validatePassword(password)) {
    showError(passwordError, 'กรุณาป้อนรหัสผ่านให้ถูกต้อง.');
    return;
  }

  form.submit();
});
// eslint-disable-next-line no-unused-vars
email.addEventListener('input', (event) => {
  removeError(emailError);
});
// eslint-disable-next-line no-unused-vars
password.addEventListener('input', (event) => {
  removeError(passwordError);
});
