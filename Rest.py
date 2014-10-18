import requests
import params
import services
import json
import time
import random
import threading
from datetime import datetime

noOfPosts = 0
noOfPuts = 0
noOfDeletes = 0
serviceUrl =params.baseurl+'/ws/rest'
outfile=open(params.outfile,'w')
runtimes = {}
failures = {}

"""
 Gets the oauth access token for accessing the services
"""
def getToken():
    headers = {'Source':'MobileApp'}
    payload = {'grant_type': 'password', 'client_id':params.client,
           'client_secret':'b709b7f5-84d6-412a-adcf-f6b50f24a4ee','scope':'none',
               'username':params.username,'password':params.password}
    response=requests.get(params.baseurl+"/oauth/token",headers=headers,params=payload)
    if(response.ok):
         return(response.json()['access_token'])

"""
Constucts the  headers for callling the sevices including the token
"""
def getHeaders():
    token=getToken()
    if token is None:
        print ('Error in getting token')
    else :
        return ({'Client':params.client,'Authorization':'Bearer '+token,
                      'Username':params.username,'Content-Type':'application/json'});

    
""" prepare the data for the post """

def getDataForPost(file,code):
    file=open(params.fileFolder+file,'r')
    if code is not None:
        jsonData =json.load(file)
        jsonData[service[3]]=params.codePrefix+str(i);
        return(json.dumps(jsonData))
    else : return(file.read())
    

"""  Calls the get service """

def callGetService(relativeUrl,requestParams):
    headers=getHeaders()
    if headers is not None :
        response=requests.get(serviceUrl+relativeUrl,headers=headers,params=requestParams)
        return(response.status_code,response.text)
    
"""  Calls the delete service """

def callDeleteService(relativeUrl,requestParams,header):
    if header is not None :
        response=requests.delete(serviceUrl+relativeUrl,headers=header,params=requestParams)
        return(response.status_code,response.text)
        
""" Calls any post service  with the request file """

def callPostService(relativeUrl,requestData,header):
    if header is not None :
        response=requests.post(serviceUrl+relativeUrl,headers=header,data=requestData)
        return(response.status_code,response.text)

""" Calls any put service  with the request file """

def callPutService(relativeUrl,requestData,header):
    if header is not None :
        response=requests.put(serviceUrl+relativeUrl,headers=header,data=requestData)
        return(response.status_code,response.text)

""" calls a service and log the time and response """    

def callAndLogservice (service,method,*args):
    t1 = datetime.now()
    response = method(*args)
    t2 = datetime.now()
    delta = t2 - t1
    combined = delta.seconds + delta.microseconds/1E6
    if not outfile.closed :
        if(response  is not None and (response[0] == 200 or response[0] == 204)):
            outfile.write(str(response[0])+':'+ service+',time :'+str(combined)+'\n')
        else :
            outfile.write(str(response[0])+':'+ service+',time :'+str(combined)+' : response :'+response[1]+'\n')
            if(service not in failures.keys()):
                failures[service] = 1
            else:
                failures[service] = failures[service] + 1
    if(service not in runtimes.keys()):
        runtimes[service] = [combined]
    else:
        runtimes[service].append(combined)
    return(response)

""" Start a user """
def startUser(userid,service,minutes):
    startTime=datetime.now()
    print('User :'+str(userid+1)+' started \n')
    while True:
            time.sleep(30+random.randint(0,30))
            response = (callAndLogservice('post',callPostService,service[0],getDataForPost(service[2],service[3]),getHeaders()))
            if(response[0] == 200):
                    # Call the put service for update
                    time.sleep(30+random.randint(0,30))
                    response = (callAndLogservice('put',callPutService,service[0],response[1],getHeaders()))
                    if(response[0] == 200):
                            jsonData=json.loads(response[1])
                            # calls the delete service
                            for jsonitem in jsonData :
                                    time.sleep(random.randint(0,30))
                                    rparams={'ohmCaseId':jsonitem['ohmCaseId'],'ohmLostWorkId':jsonitem['ohmLostWorkId']}
                                    response = (callAndLogservice('del ',callDeleteService,service[0],rparams,getHeaders()))
            currentTime=datetime.now()
            if ((currentTime-startTime).seconds/60)>= minutes :
                break
 
""" Main """          
if __name__ == "__main__":
    print('How many concurrent users you want?')
    users =int(input())
    print('How many minutes you want to run ?')
    times =int(input())
    for service in services.serviceList:
        startTime=datetime.now()
        for i in range(users):
           threading.Thread(target=startUser ,args=(i,service,times)).start()
        time.sleep((times+1)*60)
        endTime=datetime.now()
        print (service[0])
        print ("-----------------------------------------------------")
        print ("Start      :",str(startTime))
        print ("End        :",str(endTime))
        print ("Users      :",users)
        print ("Statistics : \n")
        for key in runtimes.keys():
            values=runtimes[key]
            minValue=min(values)
            maxValue=max(values)
            average=sum(values)/len(values)
            noofailures = 0;
            if key in failures.keys() :
               noofailures=failures[key] 
            print(key ,": Runs :",len(values)," Failures :",noofailures," ,Average ;",average,",Min :",minValue,",Max:",maxValue)
            outfile.write(key +": Runs :"+str(len(values))+" ,Average ;"+str(average)+",Min :"+str(minValue)+",Max:"+str(maxValue)+'\n')
    outfile.close()
            
            
     



