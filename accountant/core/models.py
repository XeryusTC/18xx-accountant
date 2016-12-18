# -*- coding: utf-8 -*-
from django.db import models
import uuid

class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
