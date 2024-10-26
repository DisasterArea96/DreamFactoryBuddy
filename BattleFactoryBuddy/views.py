from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import BattleFactoryBuddy.SetQueryHandler as SetQueryHandler
import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.SpeedQueryHandler as SpeedQueryHandler
from time import perf_counter

# This is landing on the first page.
def index(request):    
    context = {}
    context["outputstr"] = ""
    context["moves"] = StaticDataHandler.StaticDataHandler.getMoveHTML()    
    context["items"] = StaticDataHandler.StaticDataHandler.getItemHTML()
    context["pkmn"] = StaticDataHandler.StaticDataHandler.getSpeciesHTML()
    context["version"] = StaticDataHandler.StaticDataHandler.getVersion()
    return render(request, 'BattleFactoryBuddy/index.html',context)

# This is processing a request on the main Buddy function.
@csrf_exempt
def setcalc(request):
    if request.method == 'POST':        
        t1_start = perf_counter() 
        context = request.POST.dict()
        setQueryHandler = SetQueryHandler.SetQueryHandler(context)
        context = setQueryHandler.handleQuery()
        context["moves"] = StaticDataHandler.StaticDataHandler.getMoveHTML()    
        context["items"] = StaticDataHandler.StaticDataHandler.getItemHTML()
        context["pkmn"] = StaticDataHandler.StaticDataHandler.getSpeciesHTML()    
        context["version"] = StaticDataHandler.StaticDataHandler.getVersion()     
        t1_stop = perf_counter() 
        print("Elapsed time: ", t1_stop - t1_start)
        return render(request, 'BattleFactoryBuddy/index.html', context)
    else:        
        return redirect('index')

# This is processing a request for speed tiers
@csrf_exempt
def speedcalc(request):
    if request.method == 'POST':        
        t1_start = perf_counter() 
        context = request.POST.dict()                
        context = SpeedQueryHandler.SpeedQueryHandler.calcSpeedOutputs(context)     
        context["version"] = StaticDataHandler.StaticDataHandler.getVersion()   
        t1_stop = perf_counter() 
        print("Elapsed time: ", t1_stop - t1_start)
        return render(request, 'BattleFactoryBuddy/speedcalc.html', context)
    else:
        context = {}
        context["version"] = StaticDataHandler.StaticDataHandler.getVersion()
        return render(request, 'BattleFactoryBuddy/speedcalc.html', context)
