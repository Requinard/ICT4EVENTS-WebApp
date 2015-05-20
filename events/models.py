# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=510, blank=True, null=True)
    name = models.CharField(max_length=510, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Event(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    eventname = models.CharField(max_length=64)
    eventlocation = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    begintime = models.DateField()
    endtime = models.DateField()

    class Meta:
        managed = True
        db_table = 'event'


class Item(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    eventid = models.ForeignKey(Event, db_column='eventid')
    itemtype = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    amount = models.BigIntegerField()
    placelocation = models.CharField(max_length=64, blank=True, null=True)
    placecategory = models.CharField(max_length=64, blank=True, null=True)
    placecapacity = models.FloatField(blank=True, null=True)
    typeofobject = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class Likes(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', db_column='userid')
    postid = models.ForeignKey('Post', db_column='postid')

    class Meta:
        managed = False
        db_table = 'likes'


class Payment(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    registratioid = models.ForeignKey('Registration', db_column='registratioid')
    datetime = models.DateField()
    amount = models.FloatField(blank=True, null=True)
    paymenttype = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'payment'


class Post(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', db_column='userid')
    eventid = models.ForeignKey(Event, db_column='eventid')
    replyid = models.ForeignKey('self', db_column='replyid', blank=True, null=True)
    postcontent = models.TextField()
    pathtofile = models.TextField(blank=True, null=True)
    datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'post'


class Registration(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', db_column='userid')
    eventid = models.ForeignKey(Event, db_column='eventid')

    class Meta:
        managed = False
        db_table = 'registration'


class Report(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    postid = models.ForeignKey(Post, db_column='postid')
    userid = models.ForeignKey('Users', db_column='userid')
    reason = models.TextField()
    datetime = models.DateField()
    status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'report'


class Reservation(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', db_column='userid')
    itemid = models.ForeignKey(Item, db_column='itemid')
    returndate = models.DateField()
    amount = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'reservation'


class Rfidlog(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', db_column='userid')
    eventid = models.ForeignKey(Event, db_column='eventid')
    datetime = models.DateField()
    inorout = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'rfidlog'


class Tag(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    tagname = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class Tagpost(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    tagid = models.ForeignKey(Tag, db_column='tagid')
    postid = models.ForeignKey(Post, db_column='postid')

    class Meta:
        managed = False
        db_table = 'tagpost'


class Users(models.Model):
    ident = models.BigIntegerField(primary_key=True)
    rfidnumber = models.CharField(max_length=16)
    address = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=256)
    telephonenumber = models.CharField(max_length=32)
    userpassword = models.TextField()
    userlevel = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'
