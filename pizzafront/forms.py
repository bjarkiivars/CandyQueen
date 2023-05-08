from django import forms
from pizzafront.models import User

class RegisterForm(forms.ModelForm):

    '''
    RegisterForm is a form for creating a new user. It inherits from ModelForm
    and includes necessary fields for a user. It validates the input, checks password confirmation,
    and saves the user instance to the database.
    '''

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = [
            'name', 
            'email', 
            'phone_number', 
            'street_name', 
            'house_number',
            'city',
            'postal_code',
            'password',
            'img'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
