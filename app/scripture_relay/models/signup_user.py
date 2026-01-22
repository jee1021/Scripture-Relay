import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class SignUP_User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN    = "ADMIN",  "교회 임원진"
        LEADER   = "LEADER", "청년부 리더"
        MEMBER   = "MEMBER", "일반 청년부원"
        VISITOR  = "VISITOR", "손님/초대자"


    email = models.EmailField(
            _("이메일"),
            unique=True,
            db_index=True,
            error_messages={"unique": _("이미 사용 중인 이메일입니다.")},
        )

    nickname = models.CharField(
        _("닉네임"),
        max_length=30,
        blank=True,
        help_text=_("미입력 시 이메일 앞부분 사용"),
    )
    password = models.CharField(
        _("비밀번호"),
        max_length=30,
        blank=True,
        help_text=_("미입력시 다시입력"),
    )


    role = models.CharField(
        _("직분 / 역할"),
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
        db_index=True,
    )

    code_id = models.UUIDField(
        _("코드 ID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text=_("청년부 리더 또는 집사님이 발급한 초대/멤버십 코드 (UUID)"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("사용자")
        verbose_name_plural = _("사용자")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.display_name} ({self.role})"

    @property
    def display_name(self):
        return self.nickname or self.email.split("@")[0]