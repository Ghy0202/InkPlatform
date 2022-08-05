from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class WebpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WebPage'
    def ready(self):
        # 重写父类的方法
        autodiscover_modules('T5_model_pre.py')
        # 用到的地方：from app.T5_model_pre import predict_func
