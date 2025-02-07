from django.shortcuts import render
import json
from .models import EconomicActivity

def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)
        for item in data:
            economic_activity = EconomicActivity(
                title = item["descricao"]
            )
            economic_activity.save()
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')