import uuid
import logging
from http import HTTPStatus
from typing import Optional, List

from ninja import Router, Schema
from ninja.errors import HttpError

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

router = Router(tags=["회원가입"], auth=None)  # 회원가입은 인증 없이

User = get_user_model()  # → SignUP_User


# Request Schema
class SignUpIn(Schema):
    email: str
    nickname: Optional[str] = None
    password: str
    password_confirm: str
    role: str = "MEMBER"
    code_id: Optional[str] = None  # 초대코드로 사용할 경우 입력


# Response Schema (data를 리스트로 감싸는 스타일 유지)
class CommonSuccessResponse(Schema):
    success: bool
    message: str
    data: Optional[List[dict]] = None


@router.post(
    "/signup/",
    summary="회원가입 API",
    response={
        HTTPStatus.CREATED: CommonSuccessResponse,
        HTTPStatus.BAD_REQUEST: CommonSuccessResponse,
        HTTPStatus.CONFLICT: CommonSuccessResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: CommonSuccessResponse,
    },
)
def signup(request, payload: SignUpIn):
    """
    회원가입 처리
    - email은 필수 & 중복 불가
    - password는 8자 이상 권장 (추가 검증 가능)
    - nickname 미입력 시 email 아이디 부분 사용
    - code_id는 초대코드로 사용 시 입력 (UUID 형식)
    """
    # 1. 기본 필수값 검증
    if not payload.email:
        raise HttpError(HTTPStatus.BAD_REQUEST, "이메일은 필수 입력 항목입니다.")

    # 이메일 형식 간단 검증 (더 엄격하게 하려면 django validator 사용)
    try:
        validate_email(payload.email)
    except ValidationError:
        raise HttpError(HTTPStatus.BAD_REQUEST, "올바른 이메일 형식이 아닙니다.")

    if not payload.password:
        raise HttpError(HTTPStatus.BAD_REQUEST, "비밀번호는 필수입니다.")

    if payload.password != payload.password_confirm:
        raise HttpError(HTTPStatus.BAD_REQUEST, "비밀번호가 일치하지 않습니다.")

    # 비밀번호 길이 체크 (모델에 없으므로 여기서 최소한으로)
    if len(payload.password) < 8:
        raise HttpError(HTTPStatus.BAD_REQUEST, "비밀번호는 최소 8자 이상이어야 합니다.")

    # 2. 역할 검증
    valid_roles = [choice[0] for choice in User.Role.choices]
    if payload.role not in valid_roles:
        raise HttpError(
            HTTPStatus.BAD_REQUEST,
            f"유효하지 않은 역할입니다. 가능한 값: {', '.join(valid_roles)}"
        )

    # 3. 닉네임 처리
    nickname = (payload.nickname or "").strip()
    if not nickname:
        nickname = None  # 모델의 display_name 프로퍼티가 처리해줌

    try:
        # 4. 사용자 생성 (create_user 사용 → password 암호화됨)
        user = User.objects.create_user(
            email=payload.email.strip().lower(),
            password=payload.password,
            nickname=nickname,
            role=payload.role,
        )

        # 5. 초대 코드 처리
        if payload.code_id:
            try:
                # UUID 형식 검증 + 값 대입
                user.code_id = uuid.UUID(payload.code_id.strip())
            except ValueError:
                raise HttpError(HTTPStatus.BAD_REQUEST, "초대코드 형식이 올바르지 않습니다. (UUID)")
            # → 실제 서비스라면 여기서 InviteCode 모델 조회 & 사용여부 체크 권장

        user.save()

        # 6. 성공 응답 (data를 리스트로 감싸서 반환)
        user_data = {
            "email": user.email,
            "display_name": user.display_name,
            "role": user.role,
            "role_display": dict(User.Role.choices).get(user.role, user.role),
            "code_id": str(user.code_id) if user.code_id else None,
            "date_joined": user.date_joined.isoformat(),
        }

        return HTTPStatus.CREATED, CommonSuccessResponse(
            success=True,
            message="회원가입이 성공적으로 완료되었습니다.",
            data=[user_data]  # 리스트로 감싸기
        )

    except IntegrityError:
        raise HttpError(
            HTTPStatus.CONFLICT,
            "이미 사용 중인 이메일 주소입니다."
        )

    except ValidationError as ve:
        raise HttpError(HTTPStatus.BAD_REQUEST, f"입력값 오류: {str(ve)}")

    except Exception as e:
        logger.error("회원가입 중 예외 발생", exc_info=True)
        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "회원가입 처리 중 서버 오류가 발생했습니다. 관리자에게 문의해주세요."
        )
