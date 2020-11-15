from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 앞에 clean 을 붙여줘야 valid함수로 사용됨.
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):   # 암호화된 값끼리 비교
                return self.cleaned_data        # 공통 함수이기 때문에 전체 데이터 리턴
            else:
                self.add_error("password", forms.ValidationError("Password is wrong.")) # 에러 대상 필드 지정
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist."))


# forms.Form을 forms.ModelForm으로 변경함
# ModelForm을 많이 쓰지만 sign up 시에는 커스텀으로 짜는 게 편할 때가 많다고 함.
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # first_name = forms.CharField(max_length=80)
    # last_name = forms.CharField(max_length=80)
    # email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("User already exists with that email.")
    #     except models.User.DoesNotExist:
    #         return email

    # 정의된 필드 순서대로 clean 함수를 태우고 리턴 값을 cleaned_data에 넣기 때문에 clean_password 함수에서 password1값을 get 할 수 없음.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match.")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

