from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    name = 'chatbot'
    
    def ready(self):
        import chatbot.rag_engine
