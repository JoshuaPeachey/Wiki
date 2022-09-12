from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import random
from . import util

# TODO change redirect to to HTTPResponse 

class NewEntryForm(forms.Form):
    name = forms.CharField(label="name", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1', 'cols':'20'}))
    md = forms.CharField(label="md", widget=forms.Textarea(attrs={'class': 'form-control'}))

def index(request):
    if 'q' in request.GET.keys():
        if(request.GET['q'] in util.list_entries()):
            return render(request, f"encyclopedia/wiki/{request.GET['q']}.html", {
            "entries": util.list_entries()
        })
        
        else:
            list_entries = []
            for entry in (util.list_entries()):
                if(request.GET['q'].lower() in entry.lower()):
                    list_entries.append(entry)

            return render(request, "encyclopedia/substringSearch.html", {
                "entries": util.list_entries(),
                "sub_entries": list_entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def open_entry(request, entry_name):
    if(entry_name in util.list_entries()):
        return render(request, f"encyclopedia/wiki/{entry_name}.html", {
        "entries": util.list_entries(),
        "editable": True,
        "entry_name": entry_name
    })
    else:
        return render(request, "encyclopedia/wiki/Error.html", {
        "entries": util.list_entries()
    })

def create_new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data["name"])
            # print(form.cleaned_data["md"])
            if form.cleaned_data["name"] in util.list_entries():
                form.add_error("name", "This name already exists")
                return render(request, "encyclopedia/newPage.html", {
                    "entries": util.list_entries(),
                    "entry_form": form
                })
            else:
                # save the md file to the system
                util.save_entry(form.cleaned_data["name"], form.cleaned_data["md"])

                # convert md file to html
                util.save_md_to_html(form.cleaned_data["name"])

                return open_entry(request, form.cleaned_data["name"])

    return render(request, "encyclopedia/newPage.html", {
        "entries": util.list_entries(),
        "entry_form": NewEntryForm()
    })

def edit_entry(request, entry_name):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # save the md file to the system
            util.save_entry(form.cleaned_data["name"], form.cleaned_data["md"])

            # convert md file to html
            util.save_md_to_html(form.cleaned_data["name"])

            return HttpResponseRedirect(reverse('wiki:entry_name', kwargs={"entry_name":entry_name}))

    f = open(f"entries/{entry_name}.md")
    mdText = f.read()

    form = NewEntryForm({'name': entry_name, 'md': mdText})

    return render(request, "encyclopedia/EditPage.html", {
        "entries": util.list_entries(),
        "entry_form": form,
        "entry_name": entry_name
    }
    )

def delete_entry(request, entry_name):
    util.delete(entry_name)
    return HttpResponseRedirect(reverse('wiki:index'))


def random_entry(request):
    random_entry = random.choice(util.list_entries())
    return render(request, f"encyclopedia/wiki/{random_entry}.html", {
        "entries": util.list_entries
    })
