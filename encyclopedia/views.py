from django.shortcuts import render

from . import util
import random
import markdown2
from markdown2 import Markdown
markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, entry):
    #extract entry from url and put into util function
    content = util.get_entry(entry)
    if not content:
        return render(request, "encyclopedia/error.html", {"message": "Page doesn't exist" })
    #convert content to html from markdown
    content = markdowner.convert(content)
    return render(request, "encyclopedia/entry.html", {"entry": content, "title": entry })

def search(request):
    if request.method == "POST":
        #extract users query from search
        query = request.POST['q']   
        #enter it into get entry function - see if it returns anything
        entry_query = util.get_entry(query)
        if entry_query:
            #if it does return something, convert content to html from markdown and render page
            entry_query = markdowner.convert(entry_query)
            return render(request, "encyclopedia/entry.html", {"entry": entry_query })
        else:
            #if it doesnt return something, loop over all entries and search inside each for the query
            all_entries = util.list_entries()
            render_list = []
            for i in all_entries:
                print(i)
                #if query present in an entry, add to a list to render
                if query in i:
                    render_list.append(i)          
        return render(request, "encyclopedia/search.html", {"entries": render_list, "query": query})
    #get route
    else:
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def newpage(request):
    if request.method == "POST":
        form = util.NewPageForm(request.POST)
        print(form)
        if form.is_valid():
            #extract title from form - if it already exists, return error
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown_content"]
            entry_query = util.get_entry(title)
            if entry_query:
                return render(request, "encyclopedia/error.html", {"message": "Page already exists" })
            else:
                saved = util.save_entry(title, content)
                return entries(request, title)
        else:
            return render(request, "encyclopedia/error.html", {"message": "Page doesn't exist" })
    #get route
    else:
        #render form to page
        form = util.NewPageForm()
        return render(request, 'encyclopedia/newpage.html', {'form': form})



def editpage(request, entry):
    if request.method == "POST":
        form = util.NewPageForm(request.POST)
        if form.is_valid():
            #extract title from form - check title already exists, if not return error
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown_content"]
            entry_query = util.get_entry(title)
            if entry_query:
                #if page exists, update it with new content and then return the updated page
                saved = util.save_entry(title, content)
                return entries(request, title)
            else:
                saved = util.save_entry(title, content)
                return render(request, "encyclopedia/error.html", {"message": "Page doesnt exist" })
        else:
            return render(request, "encyclopedia/error.html", {"message": "Form not valid" })
    #get route
    else:
        #retrieve current entry for that title
        content = util.get_entry(entry)
        #generate form that is pre-populated
        form = util.edit_form(content)
        return render(request, 'encyclopedia/editpage.html', {'form': form, "title": entry})


def randompage(request):
    #get random entry by using imported random function + the list entries function
    random_entry = random.choice(util.list_entries())
    #pass this into entries function as your return
    return entries(request, random_entry)