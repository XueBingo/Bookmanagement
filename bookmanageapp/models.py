#coding:utf-8
from django.db import models

# Create your models here.

class Book_info(models.Model):
    NO     = models.IntegerField('NO', primary_key=True)
    ISBN   = models.CharField('ISBN', max_length=50, unique=True)
    title  = models.CharField('title', max_length=200)
    author = models.CharField('author', max_length=200)
    publisher = models.CharField('publisher', max_length=200)
    def __str__(self):
        return str(self.title)

class Userinfo(models.Model):
    NO       = models.IntegerField('NO', primary_key=True)
    username = models.CharField('username', max_length=50, unique=True)
    password = models.CharField('password', max_length=1000)
    name     = models.CharField("name", max_length=50)
    gender   = models.CharField('gender', max_length=7)
    age      = models.IntegerField('age')
    def __str__(self):
        return str(self.username)

class Account(models.Model):
    NO     = models.IntegerField('NO', primary_key=True)
    credit = models.DecimalField('credit', max_digits=20, decimal_places=2)
    def __str__(self):
        return str(self.NO)

class Sale(models.Model):
    NO     = models.OneToOneField('Book_info', to_field='NO', on_delete=models.CASCADE, primary_key=True, )
    price  = models.DecimalField('price', max_digits=20, decimal_places=2)
    stock  = models.IntegerField('stock')
    def __str__(self):
        return str(self.NO)

class Order(models.Model):
    NO     = models.IntegerField('NO', primary_key=True)
    Book_NO= models.ForeignKey('Book_info', to_field='NO', on_delete=models.CASCADE)
    user_NO   = models.ForeignKey('Userinfo', to_field='NO', on_delete=models.CASCADE)
    amount =  models.DecimalField('amount', max_digits=20, decimal_places=2)
    date   = models.CharField('date', max_length=11)
    number = models.IntegerField('number')
    status = models.CharField('status', max_length=10)
    def __str__(self):
        return str(self.NO)
