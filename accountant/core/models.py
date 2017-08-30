# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import uuid

colors = ('red', 'pink', 'purple', 'deep purple', 'indigo', 'blue',
    'light blue', 'cyan', 'teal', 'green', 'light green', 'lime', 'yellow',
    'amber', 'orange', 'deep orange', 'brown', 'grey', 'blue grey')
shades = (50,) + tuple(range(100, 1000, 100))
color_options = ('black', 'white') + \
    tuple(('{} {}'.format(c, s) for c in colors for s in shades))

class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    cash = models.IntegerField(default=12000)
    pool_shares_pay = models.BooleanField(default=False)
    ipo_shares_pay = models.BooleanField(default=False)
    log_cursor = models.OneToOneField('LogEntry', related_name='+',
        default=None, null=True, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return 'Game {}'.format(self.uuid)


class Player(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=16, default='Player')
    game = models.ForeignKey(Game, related_name='players')
    cash = models.IntegerField(default=0)

    class Meta:
        unique_together = (('game', 'name'),)

    def __str__(self):
        return self.name


class Company(models.Model):
    COLOR_CODES = tuple(((opt.replace(' ', '-'), opt.title())
        for opt in color_options))

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=8, default='Company')
    game = models.ForeignKey(Game, related_name='companies')
    text_color = models.CharField(max_length=16, choices=COLOR_CODES,
        default='black', blank=False)
    background_color = models.CharField(max_length=16, choices=COLOR_CODES,
        default='white', blank=False)
    cash = models.IntegerField(default=0)

    share_count = models.IntegerField(default=10)
    ipo_shares = models.IntegerField(default=None)
    bank_shares = models.IntegerField(default=0)
    player_owners = models.ManyToManyField(Player, related_name='shares',
        through='PlayerShare')
    company_owners = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='shares',
        through='CompanyShare',
        through_fields=('company', 'owner'),
    )

    class Meta:
        unique_together = (('game', 'name'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.ipo_shares == None:
            self.ipo_shares = self.share_count
        super(Company, self).save(*args, **kwargs)


class PlayerShare(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    owner = models.ForeignKey(Player, related_name='share_set')
    company = models.ForeignKey(Company)
    shares = models.IntegerField(default=1)

    class Meta:
        unique_together = (('owner', 'company'),)

    @property
    def game(self):
        return self.company.game


class CompanyShare(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    owner = models.ForeignKey(Company, related_name='share_set')
    company = models.ForeignKey(Company)
    shares = models.IntegerField(default=1)

    class Meta:
        unique_together = (('owner', 'company'),)

    @property
    def game(self):
        return self.company.game


class LogEntry(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    game = models.ForeignKey(Game, related_name='log')
    time = models.DateTimeField(default=timezone.now)
    text = models.TextField(default='')
    acting_company = models.ForeignKey(Company, related_name='+', null=True,
        default=None)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return '[{}] {}'.format(self.time, self.text)
