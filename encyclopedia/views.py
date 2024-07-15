from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from . import util
import markdown
from django import forms
from django.urls import reverse
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    if content is None:
        raise Http404

    httpContent = markdown.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry.capitalize(),
        "entry": httpContent
    })

class newPage(forms.Form):
    entry_title = forms.CharField(label="New Page Title", required=True,  widget=forms.TextInput(attrs={'class': 'form-title'}))
    entry_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-content'}), label="Content", required=True)

def create(request):
    if request.method == 'POST':
        new_page = newPage(request.POST)
        if new_page.is_valid():
            entry_title = new_page.cleaned_data["entry_title"].capitalize()
            entry_content = new_page.cleaned_data["entry_content"]
            all_entries = [entry.capitalize() for entry in util.list_entries()]
            
            if entry_title not in all_entries:
                util.save_entry(entry_title, entry_content)
                return HttpResponseRedirect(reverse('entry', args=[entry_title]))
            else:
                new_page.add_error('entry_title', 'This title already exists.')
    else:
        new_page = newPage()

    return render(request, "encyclopedia/create.html", {
        "form": new_page
    })

def random_page(request):
    entries = util.list_entries()
    if entries == None:
        raise Http404("No entries found")
    
    i = randint(0, len(entries) - 1)
    entry = entries[i]
    
    return HttpResponseRedirect(reverse('entry', args=[entry]))
