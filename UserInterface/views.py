from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from time import sleep 


client = OpenAI(api_key="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")
assistant = client.beta.assistants.retrieve("asst_T51X3ZCzkObwCbwXb78XLsDv")
def Sarcastic(msg):
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
    