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

