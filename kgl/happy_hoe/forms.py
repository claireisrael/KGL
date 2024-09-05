from django import forms
from .models import Sale, Stock
# This is my form for managing sales, using a ModelForm
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale  # This form is based on the Sale model
        fields = ['quantity', 'amount_received', 'issued_to', 'date', 'sale_type']  # Fields to include in the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Customizing the date input
        }

# This is my form for adding stock to the inventory
class AddForm(forms.ModelForm):
    class Meta:
        model = Stock  # This form is based on the Stock model
        fields = ['total_quantity']  # Fields to include in the form