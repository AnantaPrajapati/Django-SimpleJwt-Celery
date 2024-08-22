from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import Token, AccessToken
from .models import UserData
from rest_framework.exceptions import AuthenticationFailed

class IsAuthenticatedWithJWT(BaseAuthentication):
    def authenticate(self, request):
        # import pdb
        # pdb.set_trace()
        jwt_token = request.COOKIES.get('jwt')

        if not jwt_token:
            return None
        
        try:
            #decoding token
            access_token = AccessToken(jwt_token)
            # print("Decoded token claims:", access_token) 
            # #gets the user id by decoding code
            user_id = access_token.get('user_id')
            # print(f"Extracted user_user_id: {user_id}")
             
            #filters the id of the user
            user = UserData.objects.filter(id = user_id).first()
            # print(f"User : {user}")

            if user and user.is_authenticated:

                return (user, jwt_token)
            else:
                raise AuthenticationFailed('No user found or user not authenticated')
        
        
        except Exception as e:
             print(f"Authentication error: {e}")
             raise AuthenticationFailed('Invalid token or error decoding the token')
        
    def authenticate_header(self, request):
        return 'Bearer'