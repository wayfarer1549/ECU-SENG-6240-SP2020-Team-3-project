from django.shortcuts import render, redirect
from .models import Contract
from django.http import HttpResponse
from . import forms

def contract_list(request):
    contracts = Contract.objects.all().order_by('date')
    return render(request, 'contracts/contract_list.html', { 'contracts': contracts })

def contract_detail(request, slug):
    # return HttpResponse(slug)
    contract = Contract.objects.get(slug=slug)
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