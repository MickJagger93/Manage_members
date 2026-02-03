function togglePasswordVisibility(toggleButtonId, inputId) {
    document.getElementById(toggleButtonId).addEventListener('click', function() {
        const input = document.getElementById(inputId);
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
        this.textContent = type === 'password' ? '👁️' : '🙈';
    });
}

window.addEventListener('DOMContentLoaded', () => {
    
    const passwordDiv = document.getElementById('password-input').parentElement;
    const confirmPasswordDiv = document.getElementById('confirm-password-input').parentElement;

    const togglePassBtn = document.createElement('button');
    togglePassBtn.type = 'button';
    togglePassBtn.id = 'toggle-password';
    togglePassBtn.setAttribute('aria-label', 'Mostrar contraseña');
    togglePassBtn.style = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background:none; border:none; cursor:pointer;';
    togglePassBtn.textContent = '👁️';
    passwordDiv.appendChild(togglePassBtn);

    const toggleConfirmBtn = document.createElement('button');
    toggleConfirmBtn.type = 'button';
    toggleConfirmBtn.id = 'toggle-confirm-password';
    toggleConfirmBtn.setAttribute('aria-label', 'Mostrar confirmación de contraseña');
    toggleConfirmBtn.style = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background:none; border:none; cursor:pointer;';
    toggleConfirmBtn.textContent = '👁️';
    confirmPasswordDiv.appendChild(toggleConfirmBtn);

    togglePasswordVisibility('toggle-password', 'password-input');
    togglePasswordVisibility('toggle-confirm-password', 'confirm-password-input');

    const nameInput = document.querySelector('input[name="name"]');
    if(nameInput) nameInput.focus();

    const form = document.querySelector('form.form-style');
    form.addEventListener('submit', function () {
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
    });

    document.querySelectorAll('.error-message, .success-message').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 500);
        }, 4000);
    });
});