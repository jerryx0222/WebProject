from IntaiWeb import models
from django.db.models import Count

def GetProductList(tID):
    temp_list = models.Shiptable.objects.filter(TypeID=tID)
    productIDs = []
    for obj in temp_list:
        productIDs += [obj.ProductID]
        #print(productIDs)
    return models.Product.objects.filter(TypeID=tID, ProductID__in=productIDs)

def GetPartList(tID, pID):
    part_list = models.Titles.objects.filter(TypeID=tID, ProductID=pID)
    if part_list.count() > 0:
        return part_list

    temp_list = models.Titles.objects.filter(TypeID=tID, Members=pID)
    if temp_list.count() > 0:
        member_list = models.Titles.objects.filter(TypeID=tID, ProductID=temp_list[0].ProductID)
        partIDs = []
        for obj in member_list:
            partIDs += [obj.Members]
        part_list = models.Part.objects.filter(TypeID=tID, PartID__in=partIDs)
        return part_list

    return temp_list