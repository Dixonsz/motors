// Toggle show/hide password
function togglePassword(fieldId, btn) {
  const input = document.getElementById(fieldId);
  const icon = btn.querySelector('.material-symbols-outlined');
  if (input.type === 'password') {
    input.type = 'text';
    icon.textContent = 'visibility_off';
  } else {
    input.type = 'password';
    icon.textContent = 'visibility';
  }
}

const newPasswordInput = document.getElementById('new_password');
if (newPasswordInput) {
  newPasswordInput.addEventListener('input', function () {
    const val = this.value;

    updateCheck('check-length', val.length >= 8);
    updateCheck('check-case', /[a-z]/.test(val) && /[A-Z]/.test(val));
    updateCheck('check-number', /[0-9!@#$%^&*]/.test(val));
  });
}

function updateCheck(id, passed) {
  const el = document.getElementById(id);
  if (!el) {
    return;
  }
  const icon = el.querySelector('.material-symbols-outlined');
  if (passed) {
    icon.textContent = 'check_circle';
    el.classList.remove('text-on-surface-variant');
    el.classList.add('text-green-600');
  } else {
    icon.textContent = 'radio_button_unchecked';
    el.classList.remove('text-green-600');
    el.classList.add('text-on-surface-variant');
  }
}
