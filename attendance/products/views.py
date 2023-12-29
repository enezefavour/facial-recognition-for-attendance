from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm, RawProductForm

from .models import Product, Attendance, People
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from datetime import datetime, date
from django.conf import settings

# Create your views here.
def product_detail_view(request):
    obj = Product.objects.get(id=1)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description
    # }
    context = {
        'object': obj
    }
    return render(request, "products/product_detail.html", context)

def product_create_view(request):
    form = RawProductForm()
    context = {
        'form': my_form
    }
    return render(request, "products/product_create.html", context)

@csrf_exempt
def register_new_face(request):
    message = "Face not registered"
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # name = body["name"]

        image_b64 = body["image"]
        img_bytes = base64.b64decode(image_b64.encode('utf-8'))

        now = datetime.now()

        new_filename = now.strftime("%Y%m%d%H%M%S")
        new_filepath = str(settings.BASE_DIR)+"\\static\\assets\\pictures\\"+new_filename+".png"
        print(new_filename)
        img_file = open(new_filepath, 'wb')
        img_file.write(img_bytes)
        img_file.close()

        People.objects.create(name=body["name"], image_path=new_filename, hashed_face=body["hash"])

        message = "Face Registered"
    else:
        print('Wrong Request Type')
    return HttpResponse(message)
