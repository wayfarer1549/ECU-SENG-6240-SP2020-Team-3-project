from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse

from .models import Contract, MinimalBlock, MinimalChain
from . import forms


def contract_list(request):
    contracts = Contract.objects.all().order_by('date')
    return render(request, 'contracts/contract_list.html', { 'contracts': contracts })

def contract_detail(request, slug):
    # return HttpResponse(slug)
    contract = Contract.objects.get(slug=slug)
    if request.method == 'POST' and str(request.user) not in contract.contractStatus :
        contract.contractStatus = "Approved by " + str(request.user) + ": " + str(timezone.now())
        contract.save()
    return render(request, 'contracts/contract_detail.html', { 'contract': contract })

# add login required here; redirect if not logged in
def contract_create(request):
    if request.method == 'POST':
        form = forms.CreateContract(request.POST)
        if form.is_valid():
            # save contract to the db
            # save it as an instance, don't immediately commit the save
            instance = form.save(commit=False)
            instance.participant = request.user
            instance.save()
            return redirect('contracts:list')
    else:
        form = forms.CreateContract()
    return render(request, 'contracts/contract_create.html', {'form': form })

def contract_approve(request, slug):
    contract = Contract.objects.get(slug=slug)
    return render(request, 'contracts/contract_approve.html', {'contract': contract})

def get_blockchain(request):
    return render(request, 'blockchain.html', {'blockchain': blockchain})