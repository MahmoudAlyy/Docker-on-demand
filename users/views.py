from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import os
import requests
import subprocess
from django.http import HttpResponse
from .models import *

###################33
from django.contrib import admin
#from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
import subprocess
###################
import subprocess
import time
from subprocess import Popen, PIPE,check_output,call,run
import select
import re


### try to remove # in login requeired

#@login_required
def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        u = User.objects.get(username=username)
        user_machines = u.machine.all().values()
        #print(user_machines)
        return render(request, 'home.html',{'machine':user_machines})

    else:
        return render(request, 'home.html')


def shell(request):
    #get_value = request.GET.get('q',None)

    #process = subprocess.Popen(get_value, shell=True, stdout=subprocess.PIPE)
    #for line in process.stdout:
        #print(line)
    #process.wait()
    #print (process.returncode)

    #output = os.popen(get_value).read()

    return render(request, 'shell.html')#, {'output': process.returncode, 'output2':process.stdout})




def run_image(request):
    pass


@login_required
def browse(request):
    page_number = request.GET.get('page','1')
    q = request.GET.get('q','')
    url = 'https://hub.docker.com/api/content/v1/products/search?page='+page_number+'&page_size=15&q='+q+'&type=image'
    
    headers = {'Search-Version': 'v3'}

    page = requests.get(url,headers=headers)

    summary = page.json()['summaries']

    return render(request, 'browse.html', {'summary': summary, 'page_number':page_number,'q':q})





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



###############################################



@login_required
def console(request):
    if request.user.is_authenticated:
        username = request.user.username
        instance_id = request.GET.get('id',None)
        instance_name = Machines.objects.get(instance_id=instance_id)
        #print(m)
        #u = User.objects.get(username=username)
        #user_machines = u.machine.all().values()
        #print(user_machines)
    
    return render(request, 'console.html',{'instance_name': instance_name})


@login_required
def kill(request):
    #instance_id = request.POST.get("instance_id")
    instance_id = request.GET.get('id',None)
    
    cmd = "docker kill " + instance_id
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    Machines.objects.filter(instance_id=instance_id).delete()
    
    return render(request, 'kill.html')


@login_required
def console_post(request):  


    if request.POST:
        command = request.POST.get("command")
        instance_id = request.POST.get("instance_id")
        print("cmd:",command.encode())

        
        if command != None:
            try:
                result = ""
                master, slave = os.openpty()
                SHELL = ["/bin/bash"]
                shell = subprocess.Popen(SHELL,preexec_fn=os.setsid,bufsize=5000,stdin=slave,stdout=slave,stderr=slave,universal_newlines=True)

                os.write(master, b"docker attach  " + instance_id.encode() + b" \n")
                time.sleep(0.2)
                temp=os.read(master,2048)
                  
                # execute cmd given
                os.write(master, command.encode() + b" \n")
                time.sleep(0.6)
                result=os.read(master,4200)

                # debugging
                print("ORG:\n",result,"\nORD END\n")
                data = result.decode()
                
                # if cmd was exit, try to attach again and see if it errors out
                if "exit" in command:
                    master2, slave2 = os.openpty()
                    SHELL2 = ["/bin/bash"]
                    shell2 = subprocess.Popen(SHELL2,stdin=slave2,stdout=slave2,stderr=slave2,universal_newlines=True)

                    os.write(master2, b"docker attach  " + instance_id.encode() + b" \n")
                    time.sleep(0.5)
                    temp2=os.read(master2,2048)
                    print("temp2:",temp2)
                    if "Error: No such container: "+instance_id  in temp2.decode():
                        return HttpResponse("exit")
                

            except subprocess.CalledProcessError as e:
                data = e.output       
            
            data = data.split('\n',1)[1]

            #print("AFTER ONE SPLIE:\n",data.encode(),"\nSPLIT END\n")
            #print(data.split('\n',1)[0].encode())
            if data.split('\n',1)[0] == command+" \r":
                #print(10*"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                data = data.split('\n',1)[1]


            """
            data +="x"
            out_list = data.split("\n");
            output = ""
            for s in out_list:
                output+= s[:-1] + "\n"
            try:
                output = output.split("\n",1)[1];
            except:
                pass
            output.replace("\r","")
            output = output.rstrip()
            """
            output= data ###

            ###
            ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            output=ansi_escape.sub('', output)

            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            new_out=ansi_escape.sub('', output)
            output = new_out.replace("undefined", "")                 
            ####

            #output = output.replace("\n","")
            output = output.replace("\r","")
            #output = output +"\n"

            #print("start \n",output.encode(),"\n end\n")
            #print("start \n",output,"\n end\n")

            output = output.encode().decode()

            
            if output != "":
                output = "%c(@green)%" + output + "%c()"
                pass

        else:
            output = "%c(@orange)%Try `ls` to start with.%c()"
        return HttpResponse(output)
    return HttpResponse("Unauthorized.", status=403)



@login_required
def handle(request):
    if request.method == 'POST':
        data = request.POST.get("instance_name",None)
        if data != None:
            #pulling image 
            
            cmd = "docker pull " + data
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            for line in process.stdout:
                #print(line)
                pass
            process.wait()
            #print(process.returncode)

            if process.returncode == 0: 
                cmd = "docker run -i -d -t --rm --entrypoint /bin/sh " + data
                #print(cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                instance_id, err = process.communicate()
                instance_id = instance_id.decode()[:-1]
            
                username = request.user.username
                u = User.objects.get(username=username)
                m = Machines(user=u,instance_id=instance_id,instance_name=data)
                m.save()




                return HttpResponse(instance_id)
            else:
                return HttpResponse(-1)