from django.apps import AppConfig

class FooConfig(AppConfig):
    name = 'bootcamp.auth'
    label = 'bootcamp.auth'  # <-- this is the important line - change it to anything other than the default ('foo' in this case