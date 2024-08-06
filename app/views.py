from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Asset
from .models import Asset
from .forms import AssetForm
import plotly.graph_objs as go
import yfinance as yf
import matplotlib.pyplot as plt
import io, urllib, base64

@csrf_protect
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        asset.delete()
        return redirect('assets')
    return render(request, 'confirm_delete.html', {'asset': asset})

def analysis(request):
    # Fetch all assets
    assets = Asset.objects.all()
    asset_names = [asset.name for asset in assets]
    asset_values = [asset.unit_value * asset.quantity for asset in assets]
    
    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=asset_names, values=asset_values, hole=.3)])
    
    # Generate the HTML for the graph
    graph_html = fig.to_html(full_html=False)
    
    return render(request, 'analysis.html', {'graph_html': graph_html})

def get_asset_value(asset_name):
    ticker = yf.Ticker(asset_name)
    info = ticker.history(period='1d')
    if not info.empty:
        return info['Close'].iloc[-1]
    return None

def assets(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset_name = form.cleaned_data['asset_name']
            quantity = form.cleaned_data['quantity']
            average_cost = form.cleaned_data['average_cost']
            unit_value = get_asset_value(asset_name)

            if unit_value is not None:
                asset = Asset(
                    name=asset_name,
                    quantity=quantity,
                    average_cost=average_cost,
                    unit_value=unit_value
                )
                asset.save()
                return redirect('assets')
    else:
        form = AssetForm()

    assets = Asset.objects.all()
    total_current_value = 0
    asset_values = []

    for asset in assets:
        current_unit_value = get_asset_value(asset.name)
        if current_unit_value:
            asset.unit_value = current_unit_value
            asset.save()
        total_value = asset.unit_value * asset.quantity
        total_current_value += total_value
        asset_values.append({
            'id': asset.id,
            'name': asset.name,
            'quantity': asset.quantity,
            'average_cost': asset.average_cost,
            'unit_value': asset.unit_value,
            'total_value': total_value
        })

    return render(request, 'assets.html', {
        'form': form,
        'asset_values': asset_values,
        'total_current_value': total_current_value
    })

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is a test Django app in Docker.")
