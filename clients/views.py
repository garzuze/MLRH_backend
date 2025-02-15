from django.shortcuts import render
import json
from .models import Client, EconomicActivity, State

def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        state_mappig = {
                'AC': State.AC,
                'AL': State.AL,
                'AM': State.AM,
                'BA': State.BA,
                'CE': State.CE,
                'DF': State.DF,
                'ES': State.ES,
                'GO': State.GO,
                'MA': State.MA,
                'MT': State.MT,
                'MS': State.MS,
                'MG': State.MG,
                'PA': State.PA,
                'PB': State.PB,
                'PR': State.PR,
                'PE': State.PE,
                'PI': State.PI,
                'RJ': State.RJ,
                'RN': State.RN,
                'RS': State.RS,
                'RO': State.RO,
                'RR': State.RR,
                'SC': State.SC,
                'SP': State.SP,
                'SE': State.SE,
                'TO': State.TO,
        }

        for item in data:
            state_value = state_mappig.get(item["estado"])
            economic_activity = EconomicActivity.objects.get(id=item["atividadeEconomica_id"])
            client = Client(
                id = item['id'],
                cep = item["cep"],
                city = item["cidade"],
                neighborhood = item["bairro"],
                cnpj = item["cnpj"],
                state = state_value,
                economic_activity = economic_activity,
                trade_name = item["nomeFantasia"],
                corporate_name = item["razaoSocial"],
                number_of_employees = int(item["numeroEmpregados"]),
                state_registration = item["inscrEstadual"],
                address = item["endereco"]
            )
            client.save()
        return render(request, 'clients/success.html')
    return render(request, 'clients/form.html')