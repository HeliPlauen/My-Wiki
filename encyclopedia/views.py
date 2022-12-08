from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import util
import markdown2
import random


# global variables
NameList = util.list_entries()
TolowerNameList = [element.lower() for element in NameList]
RandomName = random.choice(TolowerNameList)
TITLE = ""


# the 1-st form type
class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'})) 
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control'}))


# the 2-nd form type
class NewTaskForm2(forms.Form):
    title = forms.CharField(label="") 
form2 = NewTaskForm2()


# the 3-d form type
class NewTaskForm3(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea())


# coming to the main page ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def index(request):       
    return render(request, "encyclopedia/index.html", {
        "entries": NameList, 
        "form2":form2, 
    })


# coming to the page showing the chosen article ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def chosen(request, title):

    global TITLE
    if len(TITLE) == 0:
        TITLE += title
    else:
        while(len(TITLE) != 0):
            TITLE = TITLE.replace(TITLE[len(TITLE) - 1], "")
        TITLE += title

    dirty_text = util.get_entry(title)
    text = markdown2.markdown(dirty_text)
    return render(request, "encyclopedia/chosen.html", {
        "title": title,
        "text": text,
        "form2":form2
    })


# coming to the creating articles page/ saving articles into the server +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/chosen-nobut.html", {
                "message":"You have to input the form",
                "form2":form2
            })

        title = form.cleaned_data["title"]
        text = form.cleaned_data["text"]
        if title.lower() not in TolowerNameList:
            NameList.append(title)
            with open(f"entries/{title}.md", 'w') as file:
                title2 = "#" + title + "\n"
                file.write(title2)
                file.write(text) 
            html2 = util.get_entry(title)
            text = markdown2.markdown(html2)
            return HttpResponseRedirect(f"/wiki/{title}")

        else:
            return render(request, "encyclopedia/chosen-nobut.html", {
                "message":"Such file already exists", 
                "form2":form2
            })
        
    else: 
        return render(request, "encyclopedia/create.html", {
            "form":NewTaskForm(), 
            "form2":form2
        })


# coming to the opening files by the 2-nd form page ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def search(request):
    form2 = NewTaskForm2(request.GET)      
    if not form2.is_valid():
        return render(request, "encyclopedia/chosen.html", {
            "title":"The filename was not inputed", 
            "form2":form2
        })


    title = form2.cleaned_data["title"]
    if title.lower() not in TolowerNameList:
        return render(request, "encyclopedia/chosen.html", {
            "title":"Such filename does not exist", 
            "form2":form2
        })

    global TITLE
    if len(TITLE) == 0:
        TITLE += title
    else:
        while(len(TITLE) != 0):
            TITLE = TITLE.replace(TITLE[len(TITLE) - 1], "")
        TITLE += title

    html = util.get_entry(title)
    text = markdown2.markdown(html)
    return render(request, "encyclopedia/chosen.html", {
        "title":title, 
        "text":text, 
        "form2":form2, 
    })        


# coming to the opening random article page ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def random(request):
    title = RandomName
    html = util.get_entry(title)
    text = markdown2.markdown(html)
    return render(request, "encyclopedia/chosen.html", {
        "title":title, 
        "text":text, 
        "form2":form2
    })


# coming to the editing articles are exist page/ saving changes into server +++++++++++++++++++++++++++++++++++++++++++++++++++++
def edit(request):
    title = TITLE
    if request.method == "POST":  
        form = NewTaskForm3(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/chosen-nobut.html", {
                "message":"This field may not be empty", 
                "form2":form2
            })

        text = form.cleaned_data["text"]
        with open(f"entries/{title}.md", 'w') as file:
            file.write(text) 
        html2 = util.get_entry(title)

        if not form.is_valid():
            return render(request, "encyclopedia/chosen-nobut.html", {
                "message":"This field may not be empty", 
                "form2":form2
            })
        else:
            text = markdown2.markdown(html2)
            return HttpResponseRedirect(f"/wiki/{title}")

    else:
        html2 = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form":NewTaskForm3({"text":html2}), 
            "form2":form2, 
            "TITLE":TITLE, 
            "title":title, 
            "TEXT":html2
        })
































# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def specified(request):
    form = cgi.FieldStorage()
    title = form.getlist('title')
    html = util.get_entry(title)
    return render(request, "encyclopedia/chosen.html", {
        "title":title, "text":html, "form2":form2
    })











