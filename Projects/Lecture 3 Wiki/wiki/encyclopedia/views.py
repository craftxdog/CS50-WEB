from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util


def convert_markdown_to_html(title):
    content = util.get_entry(title)
    Markdowner = Markdown()
    if content is None:
        return None
    else:
        return Markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_markdown_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The page you are looking for does not exist.",
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        html_content = convert_markdown_to_html(query)
        if html_content is None:
            allEntries = util.list_entries()
            recommendations = []
            for entry in allEntries:
                if query.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": html_content
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
        
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExists = util.get_entry(title)

        if titleExists is None:
            util.save_entry(title, content)
            html_content = convert_markdown_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "The page you are trying to create already exists."
            })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
    else:
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_markdown_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_markdown_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The page you are trying to save does not exist."
        })

def random_page(request):
    allEntries = util.list_entries()
    randomEntry = random.choice(allEntries)
    html_content = convert_markdown_to_html(randomEntry)
    return render(request, "encyclopedia/entry.html", {
        "title": randomEntry,
        "content": html_content
    })