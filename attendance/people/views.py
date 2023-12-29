from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from products.forms import EditForm
from products.models import People, Attendance

# Create your views here.

def index(request):
    persons = People.objects.all()
    context = {
        "persons":persons
    }
    # if request.method == "POST":
    #     query = request.GET.get('search')
    #     if query:
    #         postresult = People.objects.filter(name__contains=query)
    #         global result
    #         result = postresult[0]
    #         print(result)
    #         return result
    #         # context_2 = {
    #         #     'search_result': result
    #         # }
    #
    # persons = People.objects.all()
    # context = {
    #     "persons": persons,
    #     'search_result': result
    # }
    return render(request, 'index.html', context)

def detail(request):

    context = {}
    # result = None
    person_id = request.GET["id"]
    person = People.objects.all().filter(id=person_id)
    detail = Attendance.objects.all().filter(person=person_id)

    person_details = None
    attendance_details = None
    if person.count() > 0:
        person_details = person[0]
    if detail.count() > 0:
        attendance_details = detail

    if request.method == "POST":
        if "person_id" in request.POST:
            name = request.POST["names"]
            gender = request.POST["gender"]

            # start_date = request.POST["start_date"]
            # end_date = request.POST["end_date"]
            People.objects.all().filter(id=person_id).update(
                name=name,
                gender=gender
            )
            return redirect('people_index')

        if "search" in request.POST:
            # name = request.POST["search"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            result = Attendance.objects.filter(person_id = person_id, time_in__range=[start_date, end_date])
            print(result)
            attendance_details = result
        #

            person_id = request.GET["id"]



    context = {
        "person": person_details,
        "attendance": attendance_details,
    }


    return render(request, 'details.html', context)

def show_attendance(request):
    person = Attendance.objects.all()
    if request.method == "POST":
        print(request.POST)
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        result = Attendance.objects.filter(person__name__contains=name, time_in__range=[start_date, end_date])
        context = {
            "persons": result
        }
    else:
        context = {
            "persons": person

        }

    return render(request, 'attendance.html', context)
def search(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        result = Attendance.objects.filter(person__name__contains=name, time_in__range=[start_date, end_date])
        context = {
            "result": result
        }
        return render(request, 'advanced_search.html', context)