function togglePasswordVisibility(toggleButtonId, inputId) {
    document.getElementById(toggleButtonId).addEventListener('click', function() {
        const input = document.getElementById(inputId);
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
        this.textContent = type === 'password' ? '👁' : '🙈';
    });
}

window.addEventListener('DOMContentLoaded', () => {
    
    const newPasswordDiv = document.getElementById('new-password-input').parentElement;
    const confirmNewPasswordDiv = document.getElementById('confirm-new-password-input').parentElement;

    const toggleNewPassBtn = document.createElement('button');
    toggleNewPassBtn.type = 'button';
    toggleNewPassBtn.id = 'toggle-new-password';
    toggleNewPassBtn.setAttribute('aria-label', 'Mostrar contraseña');
    toggleNewPassBtn.style = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background:none; border:none; cursor:pointer;';
    toggleNewPassBtn.textContent = '👁️';
    newPasswordDiv.appendChild(toggleNewPassBtn);

    const toggleConfirmPassBtn = document.createElement('button');
    toggleConfirmPassBtn.type = 'button';
    toggleConfirmPassBtn.id = 'toggle-confirm-new-password';
    toggleConfirmPassBtn.setAttribute('aria-label', 'Mostrar confirmación de contraseña');
    toggleConfirmPassBtn.style = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background:none; border:none; cursor:pointer;';
    toggleConfirmPassBtn.textContent = '👁️';
    confirmNewPasswordDiv.appendChild(toggleConfirmPassBtn);

    togglePasswordVisibility('toggle-new-password', 'new-password-input');
    togglePasswordVisibility('toggle-confirm-new-password', 'confirm-new-password-input');

    const emailInput = document.querySelector('input[name="email"]');
    if(emailInput) emailInput.focus();

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