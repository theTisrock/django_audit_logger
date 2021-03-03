from django.shortcuts import render, redirect
from .models import ListItem
from .forms import ListItemForm, EditItemForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):

    if request.method == 'POST':
        form = ListItemForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Item added :)"))
            to_template = {'all_items': ListItem.objects.all}
            return render(request, 'home.html', to_template)

    else:
        to_template = {'all_items': ListItem.objects.all}
        return render(request, 'home.html', to_template)

def about(request):
    to_template = {'about_text': "This site belongs to Chris Torok"}
    return render(request, "about.html", to_template)

def delete(request, list_id):
    item = ListItem.objects.get(pk=list_id)
    item.delete()
    messages.success(request, (f"item {list_id} deleted"))
    return redirect('home')

def toggle(request, list_id):
    item = ListItem.objects.get(pk=list_id)

    item.complete = False if item.complete == True else True
    item.save()

    return redirect('home')

def edit(request, list_id: int):
    
    if request.method == 'POST':
        item = ListItem.objects.get(pk=list_id)
        form = ListItemForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()            
            messages.success(request, ("Item edited :)"))
            return redirect('home')

    else:
        to_template = {'item': ListItem.objects.get(pk=list_id)}
        return render(request, 'edit.html', to_template)

# end
