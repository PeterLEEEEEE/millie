import requests
import jwt
import json

from django.http.response import JsonResponse
from django.views import View
from django.conf import settings

from my_settings import ALGORITHM
from .models import Platform, User
from libraries.models import Library

class SocialLoginView(View):
    def post(self, request):
        try:
            access_token = request.headers.get("Authorization")
            KAKAO_API    = "https://kapi.kakao.com/v2/user/me"

            response = requests.get(
                    KAKAO_API, headers = {"Authorization" : f"Bearer {access_token}"}
                )
                
            profile_json = response.json()

            if profile_json.get('code') == -401:
                return JsonResponse({'message':'INVALID_TOKEN'}, status=401)

            kakao_id          = profile_json["id"]
            nickname          = profile_json["kakao_account"]["profile"]["nickname"]
            profile_image_url = profile_json["kakao_account"]["profile"]["profile_image_url"]

            platform = Platform.objects.get(id=1)

            user, is_user = User.objects.get_or_create(
                social_id         = kakao_id,
                nickname          = nickname,
                profile_image_url = profile_image_url,
                platform_id       = platform.id
                )

            user_id = User.objects.get(social_id=kakao_id).id
            
            if not Library.objects.filter(user_id=kakao_id).exists():
                Library.objects.create(
                    user_id = user_id
                )


            token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({"message" : "SUCCESS", "access_token" : token}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)