# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
import binascii

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string


def hash_password(created_date, password):
    salt = settings.PUB_SALT + str(time.mktime(created_date.timetuple()))[:-2]
    res = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return binascii.hexlify(res)


def get_upload_path(instance, filename):
    return '/'.join(['profile_pic', get_random_string(length=32), filename])


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    password = models.CharField('password', max_length=128)

    first_name = models.CharField('first name', max_length=200, null=True, default=None)
    last_name = models.CharField('last name', max_length=200, null=True, default=None)
    email = models.CharField('email address', max_length=200, null=True, default=None)

    phone_number = models.CharField('phone number', max_length=12, null=True, default=None)

    create_date = models.DateTimeField('creation date', default=timezone.now)
    profile_pic = models.FileField('profile pic', upload_to=get_upload_path, blank=True)

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.profile_pic.url

    @staticmethod
    def create(username, password, phone_numbers, first_name=None, last_name=None, email=None):
        user = User(username=username)
        user.save()
        now = timezone.now()

        person = Person(
            user=user,
            password=hash_password(now, password),
            create_date=now,
            phone_number=phone_numbers,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        person.save()
        return person

    def is_password_correct(self, password):
        if self.password == hash_password(self.create_date, password):
            return True
        return False

    def set_password(self, password):
        self.password = hash_password(self.create_date, password)
        self.save()

    # def login(self, password):
    #     pass

    def __unicode__(self):
        return str(self.id) + " " + self.user.username + " " + self.first_name + " " + self.last_name
