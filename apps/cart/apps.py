from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'apps.cart'


class CartMainConfig(AppConfig):
    name = 'cart'

    def ready(self):
        import cart.signals