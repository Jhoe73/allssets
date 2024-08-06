from django import forms

# Lista de ativos de interesse
ASSETS_CHOICES = [
    ('AAPL', 'Apple Inc.'),
    ('MSFT', 'Microsoft Corporation'),
    ('GOOGL', 'Alphabet Inc.'),
    ('AMZN', 'Amazon.com, Inc.'),
    ('TSLA', 'Tesla, Inc.'),
    # Adicione mais ativos conforme necessário
]

class AssetForm(forms.Form):
    asset_name = forms.ChoiceField(choices=ASSETS_CHOICES, label="Asset Name")
    quantity = forms.IntegerField(label="Quantity", min_value=1)
    average_cost = forms.DecimalField(label="Average Cost", max_digits=10, decimal_places=2)
