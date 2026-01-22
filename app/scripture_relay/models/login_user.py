from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):


    # username을 안 쓰고 싶다면 아래처럼 null/blank 허용
    username = models.CharField(
        _("사용자 이름 (선택)"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_("필수 아님. 입력하지 않으면 이메일 기반으로 표시됩니다."),
    )

    email = models.EmailField(
        _("이메일"),
        unique=True,
        db_index=True,
        error_messages={"unique": _("이미 사용 중인 이메일입니다.")},
    )

    # code_id가 정말 필요한 경우에만 추가 (권장 X)
    # 대부분의 경우 email이나 id(pk)로 충분합니다.
    code_id = models.CharField(
        _("코드 ID"),
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        help_text=_("외부 시스템 연동용 고유 코드 (선택)"),
    )

    nickname = models.CharField(
        _("닉네임"),
        max_length=30,
        blank=True,
        help_text=_("서비스 내 표시 이름 (미입력 시 이메일 앞부분 사용)"),
    )

    # 중요 설정들
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("사용자")
        verbose_name_plural = _("사용자")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return self.nickname or self.email.split("@")[0]