from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from pathlib import Path
from random import randrange
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Name", strip=True)
    content = forms.CharField(label="Description", widget=forms.Textarea)

class EditEntryForm(forms.Form):
    title = forms.CharField(label="Entry Name", strip=True, disabled=True)
    content = forms.CharField(label="Description", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):

    markdown_article = util.get_entry(title)
    if markdown_article is None:
        title = "Error"
        article = "Page does not exist."
    else:
        article = markdown(markdown_article)
    return render(request, "encyclopedia/article.html", {
        "title": title,
        "article": article,
    })

def new(request):
    if request.method == "GET":
        form = NewEntryForm()
        return render(request, "encyclopedia/edit.html", {
            "title": "Create New Page",
            "form": form,
            "action": "new",
        })
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            TitleList = util.list_entries()
            for name in TitleList:
                if name.lower() == title.lower():
                    return render(request, "encyclopedia/edit.html", {
                        "title": "Create New Page",
                        "form": form,
                        "error": "Name taken",
                        "action": "new",
                    })
            content = form.cleaned_data["content"]
            #save stuff
            entries_folder = Path("entries/")
            filename = title + ".md"
            filepath = entries_folder / filename
            file = open(filepath,"w",newline='')
            file.write(content)
            file.close()
            return HttpResponseRedirect(title)
        else:
            #form data not valid
            return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form,
            "error": "Invalid Data",
            "action": "new",
        })

def edit(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(entry)
        form = EditEntryForm(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form,
            "action": "edit",
        })
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #save stuff
            entries_folder = Path("entries/")
            filename = title + ".md"
            filepath = entries_folder / filename
            file = open(filepath,"w",newline='')
            file.write(content)
            file.close()
            return HttpResponseRedirect('/wiki/'+title)
        else:
            #form data not valid
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form,
                "error": "Invalid Data",
                "action": "edit",
            })

def search(request):
    if request.method == "GET":
        # query = request.GET["q"]
        query = request.GET.get('q')
        if util.get_entry(query) is None:
            entries = util.list_entries()
            partialList = []
            for entry in entries:
                len1 = len(entry)
                temp = entry.lower()
                for char in query:
                    temp = temp.replace(char.lower(),"",1)
                len2 = len(temp)
                if len1 == len2+len(query):
                    partialList.append(entry)
            return render(request, "encyclopedia/search.html", {
                "title": "Search",
                "entries": partialList,
            })
        else:
            return HttpResponseRedirect(query)

def random(request):
    EntryList = util.list_entries()
    randrange(0,len(EntryList)-1)
    return HttpResponseRedirect('/wiki/'+EntryList[randrange(0,len(EntryList))])