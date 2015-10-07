# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from django.test.client import Client


import logging

LOG = logging.getLogger(__name__)

class NetworkApiTestCase(TestCase):

    fixtures = ['initial_ugrupo.json',
                'initial_usuario.json',
                'initial_equip_grupos.json',
                'initial_permissions.json',
                'initial_permissoes_administrativas.json',
                'initial_direitos_grupos_equip.json']

    def setUp(self):
        pass

    def __get_http_authorization(self):
        return "Basic dGVzdDp0ZXN0"

    def tearDown(self):
        pass


