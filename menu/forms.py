from django import forms
from .models import MensajeContacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ["nombre", "email", "telefono", "asunto", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "telefono": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "asunto": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "mensaje": forms.Textarea(
                attrs={"class": "form-control form-control-sm", "rows": 3}
            ),
        }

    def clean_asunto(self):
        asunto = self.cleaned_data.get("asunto")
        if len(asunto) < 3:
            raise forms.ValidationError("El asunto debe tener al menos 3 caracteres.")
        return asunto

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get("mensaje")
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return mensaje
