# django
from django.db import models

# third packages

# your own


class TimeStampedModel(models.Model):
    # 다른 모든 모델이 상속해서 사용할 컬럼
    created = models.DateTimeField(auto_now_add=True)   # auto_now_add 옵션은 새로운 instance가 생성되면 날짜를 get해서 넣어줌
    updated = models.DateTimeField(auto_now=True)       # auto_now는 instance가 save 될때마다 날짜를 get해서 넣어줌

    class Meta:
        abstract = True     # 데이터베이스에는 생성되지 않음
