"""The View for wiki app."""
import re
import random
import markdown2


from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util



def index(request):
	"""Man should go to the home page."""
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def wiki(request, title):
	"""Page go to the wiki page."""
	data = util.handle_input(title)
	if data:
		html = markdown2.markdown(data)
		return render(request, "encyclopedia/wiki.html", {
			"text": html,
			"title": title
		})
	else:
		return HttpResponse('Page Not Found. go back to <a href="/"> home page </a>')



def edit(request, title):
	"""Edit content."""
	list_of_entries = util.list_entries()

	if title.lower() in list_of_entries:
		title = title.lower()
		return render(request, "encyclopedia/edit.html", {
			"title": title,
			"content": util.get_entry(title)
		})
	elif title.upper() in list_of_entries:
		title = title.upper()
		return render(request, "encyclopedia/edit.html", {
			"title": title,
			"content": util.get_entry(title)
		})
	elif title.title() in list_of_entries:
		title = title.title()
		return render(request, "encyclopedia/edit.html", {
			"title": title,
			"content": util.get_entry(title)
		})
	return HttpResponse('Page Not Found. go back to <a href="/"> home page </a>')

def save(request):
	"""Save content."""
	if request.method == 'POST':
		title = request.POST['entry-title']
		content = request.POST['entry-content']

	util.save_entry(title, content)
	return redirect(f'/wiki/{title}')



def rondomize_pages(request):
	"""Select random page among those pages."""
	pages_list = util.list_entries()
	randome_title = random.choice(pages_list)
	return redirect(f'/wiki/{randome_title}')


def create(request):
	"""Create new page."""
	return render(request, "encyclopedia/create.html")

def add_post(request):
	"""Add new page."""
	if request.method == 'POST':
		title = request.POST['entry-title']
		content = request.POST['entry-content']
		data = util.handle_input(title)
		if len(title) <= 0 and len(content) <= 0:
			return HttpResponse('title&amp;content field are empty. go back to <a href="/create/"> create page </a>.')
		elif len(title) <= 0:
			return HttpResponse('title field is empty. go back to <a href="/create/"> create page </a>.')
		elif len(content) <= 0:
			return HttpResponse('content field is empty. go back to <a href="/create/"> create page </a>.')
		elif data:
			return HttpResponse(f'this title is already exist . go to <a href="/wiki/{title}"> entry page </a>.')

	util.save_entry(title, content)
	return redirect('/')



def search(request):
	"""Select random page among those pages."""
	if request.method == 'GET':
		inp = request.GET['q']
		data = util.handle_input(inp)
		if data:
			return redirect(f'/wiki/{inp}')
		else:
			entries = []
			list_of_entries = util.list_entries()
			for entry in list_of_entries:
				if re.search(inp.title(), entry) or \
				   re.search(inp.upper(), entry) or \
				   re.search(inp.lower(), entry):
				   entries.append(entry)
			print(entries)
			if len(entries) > 0:
				return render(request, "encyclopedia/search.html", {
					"entries": entries
				})
			else:
				return HttpResponse('Page Not Found. go back to <a href="/"> home page </a>')


