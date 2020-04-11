from django.shortcuts import render

def contract_list(request):
    return render(request, 'contracts/contract_list.html')