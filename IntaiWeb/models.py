from django.db import models


# Create your models here.

class Part(models.Model):
    PartID = models.CharField(max_length=32, primary_key=True, default="")
    CName = models.CharField(max_length=64)
    Specification = models.CharField(max_length=128)
    Stock = models.IntegerField(default=0)
    TypeID = models.CharField(max_length=32)

    def __str__(self):
        return self.PartID

class ProcessLink(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    ProcessID = models.CharField(max_length=32)
    ProductID = models.CharField(max_length=32)
    PartID = models.CharField(max_length=32)
    theOrder = models.IntegerField(default=0)
    DayTarget = models.IntegerField(default=0)
    Stock = models.IntegerField(default=0)
    Schedule = models.IntegerField(default=0)

class SystemSet(models.Model):
    DataName = models.CharField(primary_key=True,max_length=255)
    IntData = models.IntegerField(default=0)
    DblData = models.FloatField(default=0)
    StrData = models.TextField(default='')

class Product(models.Model):
    ProductID = models.CharField(max_length=32, primary_key=True)
    CName = models.CharField(max_length=64)
    FirstPass = models.FloatField(default=0)
    Stock = models.IntegerField(default=0)
    TypeID = models.CharField(max_length=32)

    def __str__(self):
        return self.ProductID

class ProductLink(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    ProductID = models.CharField(max_length=32)
    PartID = models.CharField(max_length=32)
    PartCount = models.IntegerField(default=0)

class runningtables(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    TypeID = models.CharField(max_length=32, default="")
    ProductID = models.CharField(max_length=32, default="")
    ProcessIndex = models.IntegerField(default=0)
    ProcessID = models.CharField(max_length=32, default="")
    WipCount = models.FloatField(default=0)
    TargetCount = models.FloatField(default=0)
    SumCount = models.FloatField(default=0)



class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

class Shiptable(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    ProductID = models.CharField(max_length=32)
    ShipDate = models.CharField(max_length=16)
    TypeID = models.CharField(max_length=32)
    TargetCount = models.FloatField(default=0)
    WipCount = models.FloatField(default=0)

class Process(models.Model):
    ProcessID = models.CharField(max_length=32, primary_key=True)
    CName = models.CharField(max_length=64)

class Types(models.Model):
    TypeID = models.CharField(verbose_name="型號", max_length=32, primary_key=True, default="")
    TypeName = models.CharField(verbose_name="名稱", max_length=64)
    #TypeList = models.ForeignKey(verbose_name="型別", to_field=TypeID, on_delete=models.CASCADE)

    def __str__(self):
        return self.TypeID


class Titles(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    #TypeID = models.ForeignKey(Types, verbose_name="型別", on_delete=models.CASCADE)
    #ProductID = models.ForeignKey(Product, verbose_name="產品編號", on_delete=models.CASCADE)
    ProductID = models.CharField(max_length=32)
    TypeID = models.CharField(max_length=32)
    Members = models.CharField(max_length=32)

    def __str__(self):
        return self.TypeID

