from django.shortcuts import render, HttpResponse, redirect
from IntaiWeb import models
from IntaiWeb import LocalFunctions
from .forms import MyModelForm
from .globals import globals_Part, globals_Wip, globals_Type, globals_Part2, globals_Type2, globals_Wip2
from .globals import globals_wipType, globals_wipPart, globals_wipType1, globals_wipPart1
from .globals import globals_outType, globals_outFlag
from django import forms
from datetime import datetime
import random
import cgi

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
    global globals_outType

    tID = request.GET.get('type')  # "2ETC02"
    if tID:
        globals_outType = tID


    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData


    if not globals_outType:
            return render(request, "outputers.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists()})

    Header_list=['日期', '產品', '輸出', '庫存', '比率', '差異']
    date_list = []
    data_list = []

    temp_list = models.Shiptable.objects.filter(TypeID=globals_outType)
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
        temp_list = models.Shiptable.objects.filter(TypeID=globals_outType, ShipDate=obj)
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
                                              "Type_select": globals_outType,
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

    #print(data_list)

    return data_list



def TargetWip(request):
    global globals_wipType
    global globals_wipPart

    if request.method == 'POST':
        sumCountList = request.POST.getlist('sumcount', 'defaultData')
        #print(f"You submitted the following items: {sumCountList}")
        sumList = []
        for fSum in sumCountList:
            sumList.append(float(fSum))
        print(sumList)


    tID = request.GET.get('type')  # "2ETC02"
    if tID:
        if (globals_wipType != tID):
            globals_wipPart = ""
        globals_wipType = tID

    pID = request.GET.get('part')  # "0244D02837P02"
    if pID:
        globals_wipPart = pID

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not globals_wipType:
        return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})
    print("TypeID:" + globals_wipType)

    if not globals_wipPart:
        return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_wipType,
                                                  "Product_list": GetSelectTypeLists(globals_wipType)})
    print("ProductID:" + globals_wipPart)

    bProduct = (models.Product.objects.filter(ProductID=globals_wipPart).count() > 0)
    if (bProduct):
        Product_list = LocalFunctions.GetProductList(globals_wipType)
    else:
        Product_list = LocalFunctions.GetPartList(globals_wipType, globals_wipPart)
    if Product_list.count() <= 0:
        return HttpResponse("Product_list count=0")

    Header_list = GetTargetHeaderList(bProduct, Product_list)
    data_list = GetTargetDataList(globals_wipType, bProduct, Product_list)
    #print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    Label_list = []
    for index, item in enumerate(Header_list):
        if index != 0:
            Label_list += [item]
    #print(Label_list)

    DatasPlot1 = []
    for index, item in enumerate(data_list[0]):
        if index != 0:
            DatasPlot1 += [item]

    DatasPlot2 = []
    for index, item in enumerate(data_list[1]):
        if index != 0:
            DatasPlot2 += [item]

    DatasPlot3 = []
    for index, item in enumerate(data_list[2]):
        if index != 0:
            DatasPlot3 += [item]
    #print(DatasPlot)


    return render(request, "TargetWip.html", {"UDTime": UDTime,
                                              "Type_list": GetTypesLists(),
                                              "Type_select": globals_wipType,
                                              "Product_list": GetSelectTypeLists(globals_wipType),
                                              "Product_select": globals_wipPart,
                                              "Header_list": Header_list,
                                              "data_list": data_list,
                                              "Label_list": Label_list,
                                              "DatasPlot1": DatasPlot1,
                                              "DatasPlot2": DatasPlot2,
                                              "DatasPlot3": DatasPlot3})



def TargetWip1(request):
    global globals_wipType1
    global globals_wipPart1

    if request.method == 'POST':
        sumCountList = request.POST.getlist('sumcount', 'defaultData')
        #print(f"You submitted the following items: {sumCountList}")
        sumList = []
        for fSum in sumCountList:
            sumList.append(float(fSum))
        print(sumList)


    tID = request.GET.get('type')  # "2ETC02"
    if tID:
        if (globals_wipType1 != tID):
            globals_wipPart1 = ""
        globals_wipType1 = tID

    pID = request.GET.get('part')  # "0244D02837P02"
    if pID:
        globals_wipPart1 = pID

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not globals_wipType1:
        return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})
    print("TypeID:" + globals_wipType1)

    if not globals_wipType1:
        return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_wipType1,
                                                  "Product_list": GetSelectTypeLists(globals_wipType1)})
    print("ProductID:" + globals_wipPart1)

    bProduct = (models.Product.objects.filter(ProductID=globals_wipPart1).count() > 0)
    if(bProduct):
        print("bProduct:True")
    else:
        print("bProduct:False")
    if (bProduct):
        Product_list = LocalFunctions.GetProductList(globals_wipType1)
    else:
        Product_list = LocalFunctions.GetPartList(globals_wipType1, globals_wipPart1)
    if Product_list.count() <= 0:
        #return HttpResponse("Product_list count=0")
        return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_wipType1,
                                                  "Product_list": GetSelectTypeLists(globals_wipType1)})


    Header_list = GetTargetHeaderList(bProduct, Product_list)
    data_list = GetTargetDataList(globals_wipType1, bProduct, Product_list)
    #print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    Label_list = []
    for index, item in enumerate(Header_list):
        if index != 0:
            Label_list += [item]
    #print(Label_list)

    DatasPlot1 = []
    for index, item in enumerate(data_list[0]):
        if index != 0:
            DatasPlot1 += [item]

    DatasPlot2 = []
    for index, item in enumerate(data_list[1]):
        if index != 0:
            DatasPlot2 += [item]

    DatasPlot3 = []
    for index, item in enumerate(data_list[2]):
        if index != 0:
            DatasPlot3 += [item]
    #print(DatasPlot)


    return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                              "Type_list": GetTypesLists(),
                                              "Type_select": globals_wipType1,
                                              "Product_list": GetSelectTypeLists(globals_wipType1),
                                              "Product_select": globals_wipPart1,
                                              "Header_list": Header_list,
                                              "data_list": data_list,
                                              "Label_list": Label_list,
                                              "DatasPlot1": DatasPlot1,
                                              "DatasPlot2": DatasPlot2,
                                              "DatasPlot3": DatasPlot3})


def runningtables(request):
    global globals_Type
    global globals_Part
    global globals_Wip
    global globals_Type2
    global globals_Part2
    global globals_Wip2

    tID = request.GET.get('type')   #"2ETC02"
    if tID:
        if(globals_Type != tID):
            globals_Part=""
        globals_Type = tID

    pID = request.GET.get('part')    #"0244D02837P02"
    if pID:
        globals_Part = pID

    wipID = request.GET.get('wip')    # 1 or 0
    if wipID:
        globals_Wip = wipID

    tID2 = request.GET.get('type2')  # "2ETC02"
    if tID2:
        globals_Type2 = tID2

    pID2 = request.GET.get('part2')  # "0244D02837P02"
    if pID2:
        globals_Part2 = pID2

    wipID2 = request.GET.get('wip2')  # 1 or 0
    if wipID2:
        globals_Wip2 = wipID2

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    #if globals_Type:
    #    return render(request, "runningtables.html", {"UDTime": UDTime,
    #                                                      "Type_list": GetTypesLists()})
    print("TypeID:" + globals_Type)

    if not globals_Type2:
        globals_Type2=""
    print ("Type_select2:" + globals_Type2)

    ProductList2=GetSelectTypeLists(globals_Type2)
    print("Product_list2:" + " ".join(ProductList2))


    if not globals_Part:
        return render(request, "runningtables.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists(),
                                                      "Type_select": globals_Type,
                                                      "Product_list": GetSelectTypeLists(globals_Type),
                                                      "Type_select2": globals_Type2,
                                                      "Product_list2": ProductList2})
    print("ProductID:" + globals_Part)

    if not globals_Wip:
        globals_Wip = "1"
    print("WipData:" + globals_Wip)

    if not globals_Wip2:
        globals_Wip2 = "1"
    print("WipData2:" + globals_Wip2)

    #PartID="0244D02837P02"

    bProduct = (models.Product.objects.filter(ProductID=globals_Part).count() > 0)

    if (bProduct):
        Product_list = LocalFunctions.GetProductList(globals_Type)
    else:
        Product_list = LocalFunctions.GetPartList(globals_Type, globals_Part)

    if Product_list.count() <= 0:
        return HttpResponse("Product_list count=0")

    Header_list = GetHeaderList(bProduct, Product_list)
    data_list = GetDataList(globals_Type, globals_Wip, bProduct, Product_list)
    print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    if(len(ProductList2) >0):
        bProduct2 = (models.Product.objects.filter(ProductID=globals_Part2).count() > 0)
        if (bProduct2):
            Product_list2 = LocalFunctions.GetProductList(globals_Type2)
        else:
            Product_list2 = LocalFunctions.GetPartList(globals_Type2, globals_Part2)
        if(len(Product_list2)>0):
            Header_list2 = GetHeaderList(bProduct2, Product_list2)
            data_list2 = GetDataList(globals_Type2, globals_Wip2, bProduct2, Product_list2)
            print("Header_list2:" + str(len(Header_list2)) + ",data_list2:" + str(len(data_list2)))

            return render(request, "runningtables.html", {"UDTime": UDTime,
                                                          "Type_list": GetTypesLists(),

                                                          "Type_select": globals_Type,
                                                          "Product_list": GetSelectTypeLists(globals_Type),
                                                          "Product_select": globals_Part,
                                                          "Wip_select": globals_Wip,
                                                          "Header_list": Header_list,
                                                          "data_list": data_list,

                                                          "Type_select2": globals_Type2,
                                                          "Product_list2": ProductList2,
                                                          "Product_select2": globals_Part2,
                                                          "Wip_select2": globals_Wip2,
                                                          "Header_list2": Header_list2,
                                                          "data_list2": data_list2})


    return render(request, "runningtables.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_Type,
                                                  "Product_list": GetSelectTypeLists(globals_Type),
                                                  "Product_select": globals_Part,
                                                  "Wip_select": globals_Wip,
                                                  "Header_list": Header_list,
                                                  "data_list": data_list,
                                                  "Type_select2": globals_Type2,
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