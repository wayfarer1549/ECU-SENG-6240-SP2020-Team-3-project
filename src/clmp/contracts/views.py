from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import json, hashlib, datetime, copy
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from .models import Contract
from . import forms
from . import validate_social_security



def contract_list(request):
    contracts = Contract.objects.all().order_by('date')
    return render(request, 'contracts/contract_list.html', { 'contracts': contracts })

def contract_detail(request, slug):
    # return HttpResponse(slug)
    contract = Contract.objects.get(slug=slug)
    if request.method == 'POST' and str(request.user) not in contract.contractStatus :
        u = User.objects.get(username=request.user)
        if validate_social_security.IsTrue(u.officialidentity.SocialSecurityNumber):
            contract.contractStatus = "Approved by " + str(request.user) + ": " + str(timezone.now())
            contract.save()
            return redirect('contracts:mine_block')
    return render(request, 'contracts/contract_detail.html', { 'contract': contract })

# add login required here; redirect if not logged in
def contract_create(request):
    if request.method == 'POST':
        form = forms.CreateContract(request.POST)
        if form.is_valid():
            # save contract to the db
            # save it as an instance, don't immediately commit the save
            u = User.objects.get(username=request.user)
            if validate_social_security.IsTrue(u.officialidentity.SocialSecurityNumber):
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


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, previous_hash = '0')

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Creating our Blockchain
blockchain = Blockchain()

# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}
    return render(request, 'contracts/blockchain.html', {'chain': response })

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return render(request, 'contracts/blockchain.html', {'chain': response })

# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)   