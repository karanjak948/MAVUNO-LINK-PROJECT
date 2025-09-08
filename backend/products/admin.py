# products/admin.py

# Django Admin does NOT support mongoengine.Document models.
# Therefore, we do NOT register the Product model here.

# You can safely leave this file empty or use it for Django ORM models only.

# Example (Django ORM model):
# from django.contrib import admin
# from .models import SomeDjangoORMModel
#
# @admin.register(SomeDjangoORMModel)
# class SomeModelAdmin(admin.ModelAdmin):
#     list_display = ('field1', 'field2')
