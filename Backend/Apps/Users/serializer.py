from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CompteUtilisateur
from django.contrib.auth.models import Group, Permission

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']

class CompteUtilisateurSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CompteUtilisateur
        fields = [
            'id',
            'username',
            'email',
            'password',
            'token',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CompteUtilisateur(**validated_data)
        user.password = make_password(password)  # hash le mot de passe
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = make_password(password)  # hash si mot de passe modifié
        instance.save()
        return instance
