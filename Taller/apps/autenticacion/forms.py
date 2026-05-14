from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


INPUT_BASE = (
    "w-full pl-10 pr-4 py-3 bg-surface-container-low border-0 border-b-2 "
    "border-outline-variant font-body-md text-body-md transition-all placeholder:text-outline"
)


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su usuario',
            'class': INPUT_BASE,
            'id': 'username',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña',
            'class': INPUT_BASE,
            'id': 'password',
        })
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese su correo electrónico',
            'class': INPUT_BASE,
            'id': 'email',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('El correo electrónico es requerido.')
        return email.lower().strip()


class ConfirmResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su nueva contraseña',
            'class': INPUT_BASE,
            'id': 'new_password',
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita su nueva contraseña',
            'class': INPUT_BASE,
            'id': 'confirm_password',
        })
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        try:
            validate_password(password)  
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
