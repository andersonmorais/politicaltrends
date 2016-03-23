#from django.shortcuts import render
#from __future__ import print_function

# Create your views here.
import requests
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
import json as simplejson
from trends import connect
import urllib

#API_KEY="7d97cd9404d837c857233b35015bc6b135d3c57c"
API_KEY="c16dcd41f102364614f88d68c8f1dfb37f932c0d"
SENTIMENT="1"
OUTPUT_MODE="json"
ENDPOINT_URL="http://gateway-a.watsonplatform.net/calls/url/URLGetRankedNamedEntities"
ENDPOINT_TEXT="http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities"

def index(request):
    template = loader.get_template('trends/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

# Fetching data for a country/metric
def get_and_return_results(request):
    
    #TODO - Implement db caching per user-session
    connect.initialize()    
    
    url = request.GET.get('url')
    text = request.GET.get('text')
    
    #print("[DEBUG]: var1: %d, var2: bar %d" % (1,2))

    # Check if the result we want is stored on mongodb based on the 'url' and 'text' inputs
    if url:
        trends_from_cache = connect.get_trend_data(url, None)    
    elif text:
        trends_from_cache = connect.get_trend_data(None, text)
    else:
        ### Something went wrong.
        #trendresult = ""
        #result_data = {"trendresult": trendresult}
        #return HttpResponse(simplejson.dumps(result_data))
        return HttpResponse(simplejson.dumps(""))
     
    # If the result is not 'cached' on mongodb, call the Watson API to get the result of input analysis
    if trends_from_cache == False:
        # Get the result from Watson API
        ### URL test: http://www.theguardian.com/world/2016/mar/20/brazil-corruption-impeachment-probe
        if url:
            get_url_text=ENDPOINT_URL+"?apikey="+API_KEY+"&url="+url+"&sentiment="+SENTIMENT+"&outputMode="+ \
                OUTPUT_MODE
        elif text:
            get_url_text=ENDPOINT_TEXT+"?apikey="+API_KEY+"&text="+urllib.parse.quote(text.encode("utf8"))+"&sentiment="+SENTIMENT+"&outputMode="+ \
                OUTPUT_MODE
                   
        results = requests.get(url=get_url_text) 
        response = results.json()        
        if response['status'] == 'OK':
            # Take the most relevant politician entity in the list
            most_relevant = 0;
            mixed = False
            for entity in response['entities']:
                if 'disambiguated' in entity:
                    if entity['type']=="Person" and entity['disambiguated']:
                        if 'subType' in entity['disambiguated']:
                            for subentity in entity['disambiguated']['subType']:
                                if subentity == "Politician":
                                    if (float(entity['relevance'])) > (float(most_relevant)):
                                        most_relevant = entity['relevance']
                                        name = entity['text']
                                        sentiment = entity['sentiment']['type']
                                        if 'mixed' in entity['sentiment']:
                                            #print("[DEBUG]: mixed")
                                            if (int(entity['sentiment']['mixed'])) == 1:
                                                #print("[DEBUG]: ['sentiment']['mixed'])")
                                                mixed = True 
            # Take the entity-level most relevant sentiment and Compose final output analysis
            if most_relevant != 0:
                if mixed == True:
                    #sentiment = ['sentiment']['type']  
                    trendresult = "This text shows a UNCLEAR (POSITVE/NEGATIVE) analysis for the politician "+name.upper()+" (Most Cited Person)."                         
                else:
                    trendresult = "This text shows mostly "+sentiment.upper()+" opinion for the politician "+name.upper()+"  (Most Cited Person)."        
            else: 
                trendresult = "Politician Entity could not be found."
        else:
            trendresult = response['statusInfo']    
        
        # If result is valid or not we put it in the mongodb collection for future caching
        if url:             
            connect.store_trends_data(url, None, trendresult)
        elif text:
            connect.store_trends_data(None, text, trendresult)
#       if trendresult != '':
#             if url:
#                 connect.store_trends_data(url, None, trendresult)
#             elif text:
#                 connect.store_trends_data(None, text, trendresult)
    else: 
        # We got the results from mongodb before
        trendresult = trends_from_cache
        result_data = {"trendresult": trendresult}
        return HttpResponse(simplejson.dumps(result_data))
     
    #Dispatch the resulted calculated from Watson API
    result_data = {"trendresult": trendresult}
    return HttpResponse(simplejson.dumps(result_data))