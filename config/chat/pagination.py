from rest_framework.pagination import CursorPagination

class ChatPagination(CursorPagination):
    page_size = 30 
    ordering = '-timestamp'