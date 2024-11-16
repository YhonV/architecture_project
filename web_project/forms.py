from django import forms


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=100,required=True)
    password = forms.CharField(label='Contraseña',required=True,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña',required=True,widget=forms.PasswordInput)
    #telefono = forms.IntegerField(required=True)
    direccion = forms.CharField(max_length=200, required=True)
    # comuna = forms.CharField(max_length=50, required=True)