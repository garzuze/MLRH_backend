from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
from .models import Benefit, Client

def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        for item in data:
            print(item["cliente_id"])
            print(item["beneficio_id"])
            client = get_object_or_404(Client, id=int(item["cliente_id"]))
            benefit = Benefit.objects.get(id=int(item["beneficio_id"]))
            client.benefits.add(benefit)
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')