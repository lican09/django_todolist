#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
认证模块
"""

from django.contrib.auth.backends import ModelBackend
from todolist.models import UserProfile
from django.db.models import Q

class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            print e
        return None

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None