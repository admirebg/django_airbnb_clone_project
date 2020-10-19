from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models

# model은 데이터베이스 위에서 abstract 한 개념임

class AbstractItem(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ photo model """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

# python 은 파일을 위에서
# 밑으로 읽고, room정의가 뒤에 있기 때문에 못찾는다. but, string 형식으로 쓰면 순서 신경안써도됨.
# users의 모델일 경우 users_model.table명 으로 사용가능


class Room(core_models.TimeStampedModel):

    name = models.CharField(max_length=140) # required. no blank true.
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, related_name="rooms", on_delete=models.CASCADE)  # related_name은 역참조할때 _set 대신 사용
    room_type = models.ForeignKey(RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rule = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self): # admin의 해당 인스턴스 데이터가 템플릿에 어떻게 보여지는지 url 맵핑
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        return all_ratings/ len(all_reviews)


# >>> from users.models import User
# >>> ys = User.objects.get(username="ys")
# >>> ys.rooms_set
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'User' object has no attribute 'rooms_set'
# >>> ys.rooms
# <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x10f4799d0>
# >>> ys.rooms.all()

# foreignkey는 두 테이블간의 관계를 연결시켜준다, foreignkey는 many-to-one 관계에 사용한다. one user - many rooms.
# 연결의 시작은 room 에서 시작하며 room은 user로의 연결정보를 갖게되지만 반대로 user는 room으로의 연결정보가 없다. 그래서 _set 사용.
# foreignkey 컬럼은 pk 테이블의 id값을 갖는다. 즉 host는 user id값을 가짐.


# __str__ 메서드는
# 파이썬이 class 를 string으로 표현해야 할때 호출하는 함수임.

# on_delete=models.CASCADE
# user를 삭제하면 해당 room들도 같이 삭제됨
# cascade 가 아닌 protect면 해당 user를 갖는 room이 있으면 삭제 불가

# on_delete은 one-to-many에만 해당됨. many-to-many는 해당되지 않음. why? check하기 힘든가? todo





