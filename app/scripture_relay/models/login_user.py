import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("고유 ID"),
    )

    # username은 선택적 (필요 없으면 나중에 제거 가능)
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

    # 집사님/교회 리더가 발급하는 코드 (초대코드, 멤버 코드 등)
    code_id = models.CharField(
        _("코드 ID"),
        max_length=12,
        unique=True,
        blank=True,          # 처음 가입 시 비어있을 수 있음
        null=True,
        db_index=True,
        help_text=_("집사님 또는 청년부 리더가 발급한 코드 (로그인/초대용)"),
    )

    nickname = models.CharField(
        _("닉네임"),
        max_length=30,
        blank=True,
        help_text=_("서비스 내 표시 이름 (미입력 시 이메일 앞부분 사용)"),
    )

    # 중요 설정
    USERNAME_FIELD = "email"          # 기본 로그인 필드
    REQUIRED_FIELDS = []              # createsuperuser 시 추가 요구 필드 없음

    class Meta:
        verbose_name = _("사용자")
        verbose_name_plural = _("사용자")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return self.nickname or self.email.split("@")[0]