from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from channels.db import database_sync_to_async


class JWTAuthMiddleware:
    
    def __init__(self,app):
        self.app = app #urlrouter
    
    async def __call__(self,scope,receive,send): #runs on every websocker request 
        
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token',[None])[0]
        
        scope['user'] = await self.get_user(token)
        return await self.app(scope,receive,send)
    

    @database_sync_to_async
    def get_user(self,token):
        try:
            payload = AccessToken(token)
            return User.objects.get(id=payload['user_id'])
        except Exception:
            return None