from math import ceil
from django.utils import timezone
from django.shortcuts import render     # HttpResponse 안에 html을 보내도록 해줌. 템플릿(=html)은 렌더링한다.
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django_countries import countries
from . import models, forms
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.http import Http404



# HttpRequest & HttpResponse 는 django와 상관없이 인터넷 동작 값임
# view는 HttpResponse 를 리턴해야 함
# http request가 오면 django가 python object 로 transform해서 첫번쨰인자 request로 줌

# template이란 html이고, render함수를 써서 템플릿을 렌더링한다.
# 읽을 것 https://docs.djangoproject.com/en/2.2/ref/request-response/


def all_rooms(request):
    # print(var(request))
    # print(dir(request))
    now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>") 매번 이렇게 쓸수 없고 따라서 render를 이용해서 html을 보냄

    # print(request.GET)

    # 아래 내용을 django paginator 로 구현 가능
    # page = request.GET.get("page", 1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # page_count = ceil(models.Room.objects.count() / page_size)
    # all_rooms = models.Room.objects.all()[offset:limit]
    # return render(request, "rooms/home.html", context={"rooms": all_rooms, "page": page,
    #                                                    "page_count": page_count,
    #                                                    "page_range": range(1, page_count)})

    # django paginator
    page = request.GET.get("page")
    room_list = models.Room.objects.all()       # create queryset, but not 실행. (데이터베이스 접근 x)
    paginator = Paginator(room_list, 10)

    try:
        rooms = paginator.get_page(page)
        return render(request, "rooms/home.html", {"rooms": rooms})
    except EmptyPage:
        return redirect("/")    # redirect to home


# listView란 a page representing a list of objects
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        # return redirect("")
        # return redirect(reverse("core:home"))
        raise Http404()
    return render(request, "rooms/room_detail.html", {"room":room})



class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                # print(form.cleaned_data)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})     # form
