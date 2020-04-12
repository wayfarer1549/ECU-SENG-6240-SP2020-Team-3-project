from django.shortcuts import render
from .models import Contract

def contract_list(request):
    contracts = Contract.objects.all().order_by('date')
    return render(request, 'contracts/contract_list.html', { 'contracts': contracts })