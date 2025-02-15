from django.shortcuts import render
import json
from .models import ClientContact, Client

def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        status_choices = {
            "0": False,
            "1": True,
        }

        for item in data:
            status = status_choices.get(item["status"])
            client = Client.objects.get(id=item["cliente_id"])
            client_contact = ClientContact(
                id = item['id'],
                client = client,
                name = item["nome"],
                department = item["departamento"],
                phone = item["telefone"],
                email = item["email"],
                status = status
            )
            client_contact.save()
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')