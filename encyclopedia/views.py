from django.shortcuts import render
from django.http import Http404
from . import util
import markdown

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