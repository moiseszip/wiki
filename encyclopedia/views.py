from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from . import util
import markdown
from django import forms
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    if content == None:
        raise Http404

    httpContent = markdown.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry.capitalize(),
        "entry": httpContent
    })

class newPage(forms.Form):
    entry_title = forms.CharField(label="New Page Title", required=True)
    entry_content = forms.Textarea()

def create(request):
    all_entries = util.list_entries()

    if request.method == 'POST':
        new_page = newPage(request.POST)
        if new_page.is_valid():
            entry_title = new_page.cleaned_data["entry_title"]
            entry_content = new_page.cleaned_data["entry_content"]
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

def random(request, random):
    all_content = util.list_entries()
    random = all_content[random(0,len(all_content))]
    content = util.get_entry(random)

    if content == None:
        raise Http404
    
    httpContent = markdown.markdown(content)
    return render(request, "encyclopedia/random.html", {
        "title": random.capitalize(),
        "entry": httpContent
    })

    return HttpResponseRedirect(reverse("tasks:index"))