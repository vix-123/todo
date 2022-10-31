import imp
from rest_framework import serializers
from api.models import Todo
from django.contrib.auth.models import User


class todoserializer(serializers.ModelSerializer):
   class Meta:
    model=Todo
    fields=["task_name","User"]

class Regserializer(serializers.ModelSerializer):
   class Meta:
      model=User
      fields=["first_name","Last_name","email","username","password"]
   def create(self, validated_data):
      return User.objects.create_user(**validated_data)