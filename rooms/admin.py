from django.contrib import admin
from . import models
from django.utils.html import mark_safe


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ item admin definition """
    list_display = (
        "name",
        "used_by"
    )

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline, )

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rule"),
            },
        ),
        ("Last Details", {"fields": ("host", )}),
    )

    list_display = (
        "name",
        # "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "count_amenities",
        "count_photos",
        "total_rating"
        # "amenities",
        # "facilities",
        # "house_rule"
    )

    ordering = ("name", "price")
    list_filter = (
        "host__superhost",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rule"
    )

    row_id_fields = ("host", )  # ??
    # search에 대한 문서: https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
    search_fields = ("=city", "^host__username")

    # many to many relationship 값 생성시에 선택 box가 달라짐
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rule"
    )

    def count_amenities(self, obj):     # obj 는 current row임
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photo_set.count()

    count_amenities.short_description = "amenities count"




@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # print(type(obj.file))
        # print(dir(obj.file))

        # 그냥 html 코드는 보안상 실행하지 않음 ( 코드 인젝션으로 자원을 뺄수 있음 ) 따라서 mark_safe 로 내부 안전코드라는 걸 알려줌
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"



