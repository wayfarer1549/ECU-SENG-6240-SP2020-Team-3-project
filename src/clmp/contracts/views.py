from django.shortcuts import render
from .models import Contract
from django.http import HttpResponse

def contract_list(request):
    contracts = Contract.objects.all().order_by('date')
    return render(request, 'contracts/contract_list.html', { 'contracts': contracts })

def contract_detail(request, slug):
    return HttpResponse(slug)

# add login required here; redirect if not logged in
def contract_create(request):
    return render(request, 'contracts/contracts_create.html')