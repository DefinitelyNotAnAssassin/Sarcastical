from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from time import sleep 
import uuid 
import os 

import requests


def load_audio(message):
    url = "https://api.elevenlabs.io/v1/text-to-speech/98QrKOJxipE0eVBDZltZ"
    payload = {
        "text": message,
        "voice_settings": {
            "stability": 1,
            "similarity_boost": 1
        }
    }
    headers = {
        "xi-api-key": "cba6909d8699880887edc4769fa00dbd",
        "Content-Type": "application/json"
    }
    id = uuid.uuid4()
    fname = f"{os.getcwd()}/UserInterface/static/UserInterface/{id}.mpga"
   
    response = requests.request("POST", url, json=payload, headers=headers)
    with open(fname, 'wb') as f:
        f.write(response.content)

    return id


client = OpenAI(api_key="api_key_here")

def Sarcastic(msg):
    assistant = client.beta.assistants.retrieve("asst_T51X3ZCzkObwCbwXb78XLsDv")
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id)


    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
        if run.status == "completed":
            break      
        elif run.status == "failed":
            return False
        sleep(0.5)

    messages = client.beta.threads.messages.list(
    thread_id=thread.id,
 
    )
    return messages

def TheRelationshipSaviour(msg):
    assistant = client.beta.assistants.retrieve("asst_mw41KWFfEUQz0MEXtFjWWNMz")
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id)


    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
        if run.status == "completed":
            break      
        elif run.status == "failed":
            return False
        sleep(0.5)

    messages = client.beta.threads.messages.list(
    thread_id=thread.id,
 
    )
    return messages

def TranslateShakespeare(msg):
    assistant = client.beta.assistants.retrieve("asst_PGXCqAHTZ88Lwy8cM5mslByP")
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
       
        if run.status == "completed":
            break      
        elif run.status == "failed":
            break
        sleep(0.5)

    messages = client.beta.threads.messages.list(
    thread_id=thread.id,
 
    )
    return messages
  
# Create your views here.



def index(request):
    return render(request, 'UserInterface/index.html')

@csrf_exempt    
def chat(request):
    if request.method == 'POST':
        msg = Sarcastic(request.POST['message'])
        if msg == False:
            return HttpResponse("Request limit exceeded. Please try again later.")
        else:
            msg = msg.data[0].content[0].text.value
            return HttpResponse(f"""
                                <div class="flex items-end justify-end">
                        <div class="mr-4">
                            <p class="text-sm font-medium">Human</p>
                            <p class="text-gray-500">{request.POST["message"]}</p>
                        </div>
                        <div class="flex-shrink-0">
                            <!-- Image -->
                        </div>
                    </div>  
            <div class="flex items-start">
                        <div class="flex-shrink-0">
                        <!-- Image -->
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium">Sarcastic AI</p>
                            <p class="text-gray-500">{msg}</p>
                        </div>
                    </div>
                    
                                """)
    elif request.method == 'GET':
        return render(request, 'UserInterface/chat.html')
    else:
        return HttpResponse("Invalid request")
    
@csrf_exempt    
def TheRelationshipSaviourView(request):
    if request.method == 'POST':
        message = TheRelationshipSaviour(request.POST['message'])
        audio = load_audio(message.data[0].content[0].text.value) 
        return HttpResponse(f""" 
        <div class="flex justify-center items-center h-1/4">
            <div class="text-center">
            <p class="my-5 text-lg mb-4 mt-3  text-gray-500 font-medium">{message.data[0].content[0].text.value}</p>
            </div>
        </div>
            <audio controls autoplay style="display: none"> 
                <source src="/static/UserInterface/{audio}.mpga" type="audio/mpeg">
            </audio> 
        """)
    elif request.method == 'GET':
        return render(request, 'UserInterface/therelationshipsaviour.html')
    else:
        return HttpResponse("Invalid request")
    
@csrf_exempt
def translate(request):
    if request.method == "POST":
        msg = TranslateShakespeare(request.POST['text'])

        msg = msg.data[0].content[0].text.value
        print(msg)
       
        return HttpResponse(msg)
    elif request.method == "GET": 
        return render(request, 'UserInterface/translate.html')

    else: 
        HttpResponse("Invalid request")
    