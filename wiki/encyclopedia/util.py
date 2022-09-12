import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content.encode("utf-8")))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def save_md_to_html(filename):
    """
    Retrives an md entry by its title and creates a version of this file in html
    reference: https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html
    """
    print("\n\n\n\n here")
    with open(f"entries/{filename}.md", 'r') as f:
        text = f.read()
        # html = markdown.markdown(text)
        html = markdown2.markdown(text)
    with open(f"encyclopedia/templates/encyclopedia/wiki/{filename}.html", 'w') as f:
        f.write("{% extends 'encyclopedia/layout.html' %}\n\n{% block title %}\n")
        f.write(filename)
        f.write("\n{% endblock %}\n\n{% block body %}\n")
        f.write(html)
        f.write("\n{% endblock %}")

def delete(entry_name):
    """
    Deletes the HTML file and The CSS file with the corresponding entry name
    """
    filename = f"entries/{entry_name}.md"
    filename2 = f"encyclopedia/templates/encyclopedia/wiki/{entry_name}.html"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    
    
