from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        # before was return redirect('/'), now on page 106:
        return redirect('/lists/the-only-list-in-the-world/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    # return render(request, 'home.html',
    #               {'new_item_text': item.text}
    #               #  {'new_item_text': request.POST.get('item_text', '')}
    #               )


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
