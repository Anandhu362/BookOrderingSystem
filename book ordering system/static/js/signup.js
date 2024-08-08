const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
document.getElementById('name').addEventListener('input', function (event) {
    const input = event.target;
    const value = input.value;
    const cleanedValue = value.replace(/[^a-zA-Z\s]/g, '');
    if (value !== cleanedValue) {
        input.value = cleanedValue;
        alert('Only letters and spaces are allowed in the name field.');
    }
});