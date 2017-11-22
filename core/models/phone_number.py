# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random

import requests
from datetime import timedelta
from django.db import models

from django.utils import timezone
from django.utils.crypto import get_random_string

from core import HamkelaasyError, Error_code


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Phone_number(models.Model):
    phone_number = models.CharField('phone', max_length=15, primary_key=True)
    last_send_sms_time = models.DateTimeField('last sent sms time', default=timezone.now)

    code = models.CharField('security code', max_length=6)
    validator = models.CharField('phone number validator', max_length=30)
    is_registered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(10000, 99999))
            self.validator = get_random_string(length=29)
        if not Phone_number.represent_phone_number(self.phone_number):
            return False
            # TODO : amend this part
        super(Phone_number, self).save(args, kwargs)

    def trigger(self):
        if timezone.now() - self.last_send_sms_time < timedelta(seconds=30):
            return
        if timezone.now() - self.last_send_sms_time > timedelta(seconds=600):
            self.__re_init()

        self.__send_sms()

    def __re_init(self):
        self.code = str(random.randint(10000, 99999))
        self.validator = get_random_string(length=29)
        self.last_send_sms_time = timezone.now()
        self.save()

    def __send_sms(self):
        r = requests.post(
            "http://sms.3300.ir/services/wsSend.ashx",
            {
                'username': 'nbwa12826',
                'password': '260916',
                'mobile': self.phone_number,
                'message': unicode(self.code),
                'type': 2
            }
        )
        res = json.loads(r.text)
        if res['status'] < 0:
            return True
        if res['status'] == 103 or res['status'] == 1 or res['status'] == 2:
            raise HamkelaasyError(Error_code.Phone_number.Invalid_number)
        if res['status'] == 15:
            raise HamkelaasyError(Error_code.Phone_number.Server_in_development)

        raise HamkelaasyError(Error_code.Phone_number.Server_is_busy)

    @staticmethod
    def represent_phone_number(s):
        if not represents_int(s):
            return False

        if len(s) == 11 and s[0] == '0':
            s = '98' + s[1:]
        if len(s) == 10 and s[0] == '9':
            s = '98' + s[:]
        if len(s) != 12 or (not s[:2] == '98'):
            return False
        return True

    def __unicode__(self):
        return self.phone_number
