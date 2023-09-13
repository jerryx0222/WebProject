from django.shortcuts import render, HttpResponse
from IntaiWeb import models
from IntaiWeb import LocalFunctions
from django import forms
from datetime import datetime


# Create your views here.

def homepage(request):
    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime=obj.StrData

    #lstTypes = []
    #lstProducts = []
    #GetSelectLists(0, lstTypes, lstProducts)
    # print("Types:", lstTypes)
    # print("Products:", lstProducts)

    return render(request, "index.html", {"UDTime": UDTime})


def index(request):
    name = 'superman'
    roles = ["admin", "engineer", "operator"]
    user_info = {"name": "a1", "salary": 10000, "role": "ceo"}

    data_list = [
        {"name": "b1", "salary": 10000, "role": "ceo"},
        {"name": "b2", "salary": 20000, "role": "engineer"},
        {"name": "b3", "salary": 30000, "role": "operator"},
    ]

    return render(request, 'index.html',
                  {'n1': name,
                   'n2': roles,
                   'n3': user_info,
                   'n4': data_list})


def something(request):
    print(request.method)  # GET

    print(request.GET)

    print(request.POST)

    #models.UserInfo.objects.create(name="jack", password="1234")

    product_list = models.Shiptable.objects.all()
    for obj in product_list:
        print(obj.TypeID)



    #UserInfo.object.create(name="jackson", password='1234')

    return HttpResponse("fedback information")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("pwd")
        if username == "hcs" and password == "1234":
            return HttpResponse("login success")
        else:
            # return HttpResponse("login Failed")
            return render(request, "login.html", {"error_msg": "login failed"})

def outputers(request):
    tID = request.GET.get('type')  # "2ETC02"

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not tID:
        return render(request, "outputers.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})

    Header_list=['日期', '產品', '輸出', '庫存', '比率', '差異']
    date_list = []
    data_list = []

    temp_list = models.Shiptable.objects.filter(TypeID=tID)
    for obj in temp_list:
        bFind=False
        for date in date_list:
            if date == obj.ShipDate:
                bFind=True
                break
        if not bFind:
            date_list += [obj.ShipDate]
    #print(date_list)


    for obj in date_list:
        my_list = []
        temp_list = models.Shiptable.objects.filter(TypeID=tID, ShipDate=obj)
        index=1
        for info in temp_list:
            info_list = [index]
            info_list += [obj]
            info_list += [info.ProductID]
            info_list += [int(info.TargetCount)]
            info_list += [int(-1*info.WipCount)]
            if info.TargetCount<=0:
                info_list += [0]
            else:
                info_list += [-100*info.WipCount/info.TargetCount]
            diff=info.WipCount+info.TargetCount
            if diff>0:
                info_list += [int(diff)]
            else:
                info_list += [""]
            index=index+1
            my_list += [info_list]
        data_list += [my_list]

    #print(data_list)

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData



    return render(request, "outputers.html", {"UDTime": UDTime,
                                              "Type_list": GetTypesLists(),
                                              "Type_select": tID,
                                              "Header_list": Header_list,
                                              "data_list": data_list})




def GetHeaderList(bProduct, Product_list):
    Header_list = []

    if (bProduct):
        data_first = models.runningtables.objects.filter(ProductID=Product_list[0].ProductID)
    else:
        data_first = models.runningtables.objects.filter(ProductID=Product_list[0].Members)

    nIndex = data_first.count()
    hlist = []
    for obj in data_first:
        hlist += [str(nIndex)]
        nIndex -= 1
    hlist.reverse()
    Header_list += [hlist]

    hlist = []
    for obj in data_first:
        hlist += [obj.ProcessID]
    hlist.reverse()
    Header_list += [hlist]

    hlist = []
    for obj in data_first:
        ProcessName = models.Process.objects.filter(ProcessID=obj.ProcessID)
        for h in ProcessName:
            hlist += [h.CName]
            break
    hlist.reverse()
    Header_list += [hlist]

    return Header_list

def GetDataList(tID, wipID,bProduct,Product_list):
    data_list = []

    for obj in Product_list:
        hlist = []
        if (bProduct):
            hlist += [obj.ProductID]
            temp_list = models.Product.objects.filter(ProductID=obj.ProductID)
        else:
            hlist += [obj.Members]
            temp_list = models.Part.objects.filter(PartID=obj.Members)
        #print(temp_list)

        for name in temp_list:
            hlist += [name.CName]
            break

        if (bProduct):
            temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=obj.ProductID)
        else:
            temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=obj.Members)

        for v in reversed(temp_list):
            if (wipID != "1"):
                hlist += [v.WipCount]
            else:
                hlist += [v.TargetCount]


        data_list += [hlist]

    return data_list


def GetTargetHeaderList(bProduct, Product_list):
    Header_list = []

    if (bProduct):
        data_first = models.runningtables.objects.filter(ProductID=Product_list[0].ProductID)
    else:
        data_first = models.runningtables.objects.filter(ProductID=Product_list[0].Members)

    for obj in data_first:
        ProcessName = models.Process.objects.filter(ProcessID=obj.ProcessID)
        for h in ProcessName:
            Header_list += [h.CName]
            break
    Header_list+= ["製程"]
    Header_list.reverse()

    return Header_list
def GetTargetDataList(tID, bProduct,Product_list):
    data_list = []

    for index,obj in enumerate(Product_list):

        if (bProduct):
            temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=obj.ProductID)
        else:
            temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=obj.Members)

        if index == 0:
            hlist = []
            hlist += ["庫存"]
            for v in reversed(temp_list):
                hlist += [v.TargetCount]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[0][index2+1] += v.TargetCount

        if index == 0:
            hlist = []
            hlist += ["目標"]
            for v in reversed(temp_list):
                hlist += [v.SumCount]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[1][index2+1] += v.SumCount

        if index == 0:
            hlist = []
            hlist += ["累計"]
            for v in reversed(temp_list):
                hlist += [v.WipCount]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[2][index2+1] += v.WipCount

    print(data_list)

    return data_list

def TargetWip(request):
    tID = request.GET.get('type')  # "2ETC02"
    pID = request.GET.get('part')  # "0244D02837P02"

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not tID:
        return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists()})
    print("TypeID:" + tID)

    if not pID:
        return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists(),
                                                      "Type_select": tID,
                                                      "Product_list": GetSelectTypeLists(tID)})
    print("ProductID:" + pID)

    bProduct = (models.Product.objects.filter(ProductID=pID).count() > 0)
    if (bProduct):
        Product_list = LocalFunctions.GetProductList(tID)
    else:
        Product_list = LocalFunctions.GetPartList(tID, pID)
    if Product_list.count() <= 0:
        return HttpResponse("Product_list count=0")

    Header_list = GetTargetHeaderList(bProduct, Product_list)
    data_list = GetTargetDataList(tID, bProduct, Product_list)
    print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": tID,
                                                  "Product_list": GetSelectTypeLists(tID),
                                                  "Product_select": pID,
                                                  "Header_list": Header_list,
                                                  "data_list": data_list})


def runningtables(request):
    tID = request.GET.get('type')   #"2ETC02"
    pID = request.GET.get('part')    #"0244D02837P02"
    wipID = request.GET.get('wip')    # 1 or 0

    tID2 = request.GET.get('type2')  # "2ETC02"
    pID2 = request.GET.get('part2')  # "0244D02837P02"
    wipID2 = request.GET.get('wip2')  # 1 or 0

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not tID:
        return render(request, "runningtables.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists()})
    print("TypeID:" + tID)

    if not tID2:
        tID2=""
    print ("Type_select2:" + tID2)

    ProductList2=GetSelectTypeLists(tID2)
    print("Product_list2:" + " ".join(ProductList2))


    if not pID:
        return render(request, "runningtables.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists(),
                                                      "Type_select": tID,
                                                      "Product_list": GetSelectTypeLists(tID),
                                                      "Type_select2": tID2,
                                                      "Product_list2": ProductList2})
    print("ProductID:" + pID)

    if not wipID:
        wipID = "1"
    print("WipData:" + wipID)

    if not wipID2:
        wipID2 = "1"
    print("WipData2:" + wipID2)

    #PartID="0244D02837P02"

    bProduct = (models.Product.objects.filter(ProductID=pID).count() > 0)

    if (bProduct):
        Product_list = LocalFunctions.GetProductList(tID)
    else:
        Product_list = LocalFunctions.GetPartList(tID, pID)

    if Product_list.count() <= 0:
        return HttpResponse("Product_list count=0")

    Header_list = GetHeaderList(bProduct, Product_list)
    data_list = GetDataList(tID,wipID,bProduct,Product_list)
    print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    if(len(ProductList2) >0):
        bProduct2 = (models.Product.objects.filter(ProductID=pID2).count() > 0)
        if (bProduct2):
            Product_list2 = LocalFunctions.GetProductList(tID2)
        else:
            Product_list2 = LocalFunctions.GetPartList(tID2, pID2)
        if(len(Product_list2)>0):
            Header_list2 = GetHeaderList(bProduct2, Product_list2)
            data_list2 = GetDataList(tID2, wipID2, bProduct2, Product_list2)
            print("Header_list2:" + str(len(Header_list2)) + ",data_list2:" + str(len(data_list2)))

            return render(request, "runningtables.html", {"UDTime": UDTime,
                                                          "Type_list": GetTypesLists(),

                                                          "Type_select": tID,
                                                          "Product_list": GetSelectTypeLists(tID),
                                                          "Product_select": pID,
                                                          "Wip_select": wipID,
                                                          "Header_list": Header_list,
                                                          "data_list": data_list,

                                                          "Type_select2": tID2,
                                                          "Product_list2": ProductList2,
                                                          "Product_select2": pID2,
                                                          "Wip_select2": wipID2,
                                                          "Header_list2": Header_list2,
                                                          "data_list2": data_list2})


    return render(request, "runningtables.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": tID,
                                                  "Product_list": GetSelectTypeLists(tID),
                                                  "Product_select": pID,
                                                  "Wip_select": wipID,
                                                  "Header_list": Header_list,
                                                  "data_list": data_list,
                                                  "Type_select2": tID2,
                                                  "Product_list2": ProductList2})



def GetTypesLists():
    lstTypes = []
    lstTemp = models.Titles.objects.values('TypeID').order_by('TypeID').distinct()
    for t in lstTemp:
        strTemp = t["TypeID"]
        lstTypes += [strTemp]
    return lstTypes

def GetSelectTypeLists(type):
    Product_list = []
    lstTemp = models.Titles.objects.values('TypeID').order_by('TypeID').distinct()
    for t in lstTemp:
        strTemp = t["TypeID"]
        if(strTemp==type):
            lstTemp2 = models.Titles.objects.filter(TypeID=strTemp).values('ProductID').order_by('ProductID').distinct()
            lstTemp3 = []
            for p in lstTemp2:
                lstTemp3 += [p["ProductID"]]
            Product_list+=lstTemp3
    return Product_list

def GetSelectLists(id,lstTypes,lstProducts):
    index=0
    lstTemp = models.Titles.objects.values('TypeID').order_by('TypeID').distinct()
    for t in lstTemp:
        strTemp = t["TypeID"]
        lstTypes += [strTemp]
        if index==id:
            lstTemp2 = models.Titles.objects.filter(TypeID=strTemp).values('ProductID').order_by('ProductID').distinct()
            lstTemp3 = []
            for p in lstTemp2:
                lstTemp3 += [p["ProductID"]]
            lstProducts+=lstTemp3
        index=index+1
def GetPartLists(TypeName,pID):
    lstTypes = models.Titles.objects.filter(TypeID = TypeName, ProductID=pID).values('Members').order_by('Members').distinct()
    return lstTypes

"""
class TypeModeForm(forms.ModelForm):
    class Meta:
        model = models.Titles
        fields = ['TypeID', 'ProductID']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def TypeList(request):
    form = TypeModeForm()
    return render(request, "TypeSelect.html", {"form": form})

def TypeSelect(request, gId):
    row_object = models.Types.objects.filter(TypeID=gId)
    print(row_object)
    form = TypeModeForm()
    return render(request, "TypeSelect.html", {"form": form})
"""