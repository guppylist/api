import json, requests, uuid

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from guppylist.contrib.list.models import List, ListProducts, Item
from guppylist.contrib.list.forms import ListItemAddForm


def item_add(request):
    form = ListItemAddForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            item = Item()
            item.user = request.user
            item.url = form.cleaned_data['url']
            item.title = form.cleaned_data['title']
            item.description = form.cleaned_data['description']

            # Pull image from URL
            r = requests.get(form.cleaned_data['image'])
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
            item.image.save(str(uuid.uuid4()), File(img_temp), save=True)

            # item.image = form.cleaned_data['image']
            item.save()

            return HttpResponseRedirect(item.get_url())
    else:
        True


    payload = dict(
        form=form,
    )

    return render_to_response('list/item/add.html', payload, context_instance=RequestContext(request))

def item_view(request, id):
    item = Item.objects.get(id=id)
    payload = dict(
        item=item
    )

    return render_to_response('list/item/view.html', payload, context_instance=RequestContext(request))

def lists(request, username):
    user = get_user_model().objects.get(username=username)
    lists = List.objects.all().filter(user=user)

    return render_to_response('list/lists.html', dict(lists=lists), context_instance=RequestContext(request))

def get_metadata(request):
    url = request.GET.get('url')
    meta = Item.get_metadata(url)

    return HttpResponse(json.dumps(meta), mimetype='application/json')

"""
def list(request, username, list_slug):
    user = get_user_model().objects.get(username=username)
    list = List.objects.get(user=user, slug=list_slug)
    request.page_title = '%s by %s' % (list.title, user.username)

    return render_to_response('list/list.html', dict(list=list), context_instance=RequestContext(request))

def add_form(request, product, lists):
    new_form = ListAddNewForm(request.POST or None, initial={'product_id': product.id})
    existing_form = ListAddExistingForm(request.POST or None, initial={'product_id': product.id}, user=request.user)

    payload = dict(
        new_form=new_form,
        existing_form=existing_form,
        product=product,
        lists=lists,
    )

    return render_to_response('list/add.html', payload, context_instance=RequestContext(request))

def test_form(request):
    # return HttpResponse(json.dumps({'hello': 'world'}), mimetype='application/json')

    form = ListAddExistingForm(request.POST or None, request=request)

    if request.method == 'POST':
        if form.is_valid():
            print '>>>>>>>>>>>>>>>> %s' % request.POST
            print '>>>>>>>>>>>>>>>>> FORM VALID'
        else:
            print ' >>>>>>>>>>>>>>>>> FORM NOT NOT NOT VALID'

    return render_to_response('list/test.html', dict(form=form), context_instance=RequestContext(request))

def add_new_submit(request):
    if request.method == 'POST':
        form = ListAddNewForm(request.POST or None)

        if form.is_valid():
            product = Product.objects.get(id=form.cleaned_data['product_id'])

            list = List()
            list.title = form.cleaned_data['title']
            list.description = form.cleaned_data['description']
            list.user = request.user
            list.save()

            list_products = ListProducts()
            list_products.list = list
            list_products.product = product
            list_products.user = request.user
            list_products.notes = form.cleaned_data['notes']
            list_products.save()

            response = {
                'success': True,
            }
        else:
            lists = List.objects.filter(user=request.user)
            product = Product.objects.get(id=request.POST.get('product_id'))
            form = add_form(request, product, lists).content

            response = {
                'success': False,
                'form': form,
            }

    return HttpResponse(json.dumps(response), mimetype='application/json')

def add_existing_submit(request):
    if request.method == 'POST':
        form = ListAddExistingForm(request.POST or None, user=request.user)

        print request.POST
        if form.is_valid():
            list = List.objects.get(id=form.cleaned_data['list_id'])
            product = Product.objects.get(id=form.cleaned_data['product_id'])

            list_products = ListProducts()
            list_products.list = list
            list_products.product = product
            list_products.user = request.user
            list_products.notes = form.cleaned_data['notes']
            list_products.save()

            response = {
                'success': True,
            }
        else:
            lists = List.objects.filter(user=request.user)
            product = Product.objects.get(id=request.POST.get('product_id'))
            form = add_form(request, product, lists).content

            response = {
                'success': False,
                'form': form,
            }

    return HttpResponse(json.dumps(response), mimetype='application/json')
"""

