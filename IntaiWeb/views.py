from django.shortcuts import render, HttpResponse, redirect
from IntaiWeb import models
from IntaiWeb import LocalFunctions
from .forms import MyModelForm
from .globals import globals_Part, globals_Wip, globals_Type, globals_Part2, globals_Type2, globals_Wip2
from .globals import globals_wipType, globals_wipPart, globals_wipType1, globals_wipPart1
from .globals import globals_outType, globals_outFlag, globals_loginuser
from django import forms
from datetime import datetime
import random
import cgi
import time
import os

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

def DataImport(request):
    global globals_loginuser

    SysDatas = models.SystemSet.objects.get(DataName='UpdateDateTime')
    if(SysDatas):
        UDTime = SysDatas.StrData

    if request.method == 'POST':
        globals_loginuser = ""
        if(request.POST.get('password')=="1234"):
            globals_loginuser="OK"
        #print("password:" + password)

    filePath = "C:/Users/MyUser/Downloads/"
    SysDatas = models.SystemSet.objects.get(DataName='UpdateFilePath')
    if (SysDatas):
        filePath = SysDatas.StrData
        print("filePath:" + filePath)
    else:
        print("Read Systemset Error!")

    today_date = datetime.today()
    today_date_str = today_date.strftime("%Y/%m/%d")

    Header_list = ['Date', 'Type', 'Mes', 'Count', 'Product']
    data_list = []
    data_list += [Header_list]

    for p1 in models.Product.objects.all():
        selData = models.Shiptable.objects.filter(ProductID=p1.ProductID)
        if(selData.count()<=0):
            new_ship = models.Shiptable.objects.create(ProductID=p1.ProductID, ShipDate=today_date_str, TypeID=p1.TypeID, TargetCount=0)
            new_ship.save()

    DataOutList = models.Shiptable.objects.order_by('TypeID', 'ShipDate', 'ProductID')
    for obj in DataOutList:
        ProductSelect = models.Product.objects.get(ProductID=obj.ProductID)
        Temp_list = []
        if (ProductSelect):
            Temp_list += [obj.ShipDate]
            Temp_list += [obj.TypeID]
            Temp_list += [obj.ProductID]
            Temp_list += [int(obj.TargetCount)]
            Temp_list += [ProductSelect.CName]
            #print("Date:" + obj.ShipDate + ",Type:" + obj.TypeID + ",ProductID:" + obj.ProductID + ",Count:" + str(obj.TargetCount) + ',Name:' + ProductSelect.CName)
            #print(Temp_list)
            data_list += [Temp_list]

    #print(AllData_List)




    if request.method == 'POST':
        uploaded_file = request.FILES.get('fileToUpload')
        if uploaded_file:
            strFileSave=filePath + uploaded_file.name
            print("strFileSave:" + strFileSave)
            with open(strFileSave, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            os.chmod(strFileSave, 0o777)

    return render(request, "DataImport.html", {"UDTime": UDTime,
                                               "data_list": data_list,
                                               "globals_loginuser": globals_loginuser})



def outputers(request):
    global globals_outType

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    tID = request.GET.get('type')  # "2ETC02"
    if tID:
        globals_outType = tID
    else:
        globals_outType = ""
        return render(request, "outputers.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})
    print('Type:' + globals_outType)

    allTable = request.GET.get('allTable')
    if allTable:
        print('allTable:' + allTable)




    Header_list=['日期', '產品', '輸出', '庫存', '比率', '差異']
    date_list = []
    Data_list = []

    temp_list1 = models.Shiptable.objects.filter(TypeID=globals_outType)
    for obj1 in temp_list1:
        bFind=False
        for date in date_list:
            if date == obj1.ShipDate:
                bFind=True
                break
        if not bFind:
            date_list += [obj1.ShipDate]
    #print(date_list)
    #time.sleep(1)

    for obj2 in date_list:
        my_list = []
        temp_list2 = models.Shiptable.objects.filter(TypeID=globals_outType, ShipDate=obj2)
        index = 1
        for info in temp_list2:
            info_list = [index]
            info_list += [obj2]
            info_list += [info.ProductID]
            info_list += [int(info.TargetCount)]
            info_list += [int(-1*info.WipCount)]
            if info.TargetCount <= 0:
                info_list += [0]
            else:
                info_list += [-100*info.WipCount/info.TargetCount]
            diff=info.WipCount+info.TargetCount
            if diff>0:
                info_list += [int(diff)]
            else:
                info_list += [""]
            index = index+1
            my_list += [info_list]
        Data_list += [my_list]

    #print(Data_list)

    if(len(Data_list) <= 0):
        return render(request, "outputers.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})

    return render(request, "outputers.html", {"UDTime": UDTime,
                                              "Type_list": GetTypesLists(),
                                              "Type_select": globals_outType,
                                              "Header_list": Header_list,
                                              "data_list": Data_list})




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
                hlist += [int(v.WipCount)]
            else:
                hlist += [int(v.TargetCount)]


        data_list += [hlist]

    return data_list

def GetTargetHeaderList1(ProductID):
    Header_list = []
    data_first = models.runningtables.objects.filter(ProductID=ProductID).order_by('ProcessIndex')
    #print(data_first)
    for obj in data_first:
        ProcessName = models.Process.objects.filter(ProcessID=obj.ProcessID)
        for h in ProcessName:
            Header_list += [h.CName]
            break

    Header_list += ["製程"]
    Header_list.reverse()

    return Header_list

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

def GetTargetDataList1(tID, ProductID):
    temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=ProductID).order_by('ProcessIndex')

    data_list = []
    dataL1 = []
    dataL2 = []
    dataL3 = []
    for index,obj in enumerate(reversed(temp_list)):
        if index == 0:
            dataL1 += ["庫存"]
            dataL2 += ["目標"]
            dataL3 += ["累計"]
        dataL1 += [int(obj.TargetCount)]
        dataL2 += [int(obj.SumCount)]
        dataL3 += [int(obj.WipCount)]

    data_list += [dataL1]
    data_list += [dataL2]
    data_list += [dataL3]
    return data_list

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
                hlist += [int(v.TargetCount)]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[0][index2+1] += int(v.TargetCount)

        if index == 0:
            hlist = []
            hlist += ["目標"]
            for v in reversed(temp_list):
                hlist += [int(v.SumCount)]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[1][index2+1] += int(v.SumCount)

        if index == 0:
            hlist = []
            hlist += ["累計"]
            for v in reversed(temp_list):
                hlist += [int(v.WipCount)]
            data_list += [hlist]
        else:
            for index2, v in enumerate(reversed(temp_list)):
                data_list[2][index2+1] += int(v.WipCount)

    #print(data_list)

    return data_list



def TargetWip(request):
    global globals_wipType
    global globals_wipPart

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
        #return HttpResponse("Product_list count=0")
        return render(request, "TargetWip.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_wipType,
                                                  "Product_list": GetSelectTypeLists(globals_wipType)})

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
    global globals_loginuser

    tID = request.GET.get('type')  # "2ETC02"
    if tID:
        if (globals_wipType1 != tID):
            globals_wipPart1 = ""
        globals_wipType1 = tID

    pID = request.GET.get('part')  # "0244D02837P02"
    if pID:
        globals_wipPart1 = pID

    if request.method == 'POST':
        sumCountList = request.POST.getlist('sumcount', 'defaultData')
        SaveItems = models.runningtables.objects.filter(TypeID=globals_wipType1,
                                                        ProductID=globals_wipPart1)
        if(SaveItems.count()==len(sumCountList)):
            pIndex=0
            for fSum in reversed(sumCountList):
                #print(str(pIndex) + ':' + fSum)
                SaveItem = models.runningtables.objects.get(TypeID=globals_wipType1,
                                                               ProductID=globals_wipPart1,
                                                               ProcessIndex=pIndex)
                if(SaveItem):
                    SaveItem.SumCount = float(fSum)
                    SaveItem.save()
                    #print("Save" + str(pIndex))
                pIndex=pIndex+1




    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    if not globals_wipType1:
        return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists()})
    print("TypeID:" + globals_wipType1)

    if not globals_wipPart1:
        return render(request, "TargetWip1.html", {"UDTime": UDTime,
                                                  "Type_list": GetTypesLists(),
                                                  "Type_select": globals_wipType1,
                                                  "Product_list": GetSelectTypeListsAll(globals_wipType1),
                                                   "globals_loginuser": globals_loginuser})
    print("ProductID:" + globals_wipPart1)

    Header_list = GetTargetHeaderList1(globals_wipPart1)
    #print(Header_list)

    data_list = GetTargetDataList1(globals_wipType1, globals_wipPart1)
    #print(data_list)

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
                                              "Product_list": GetSelectTypeListsAll(globals_wipType1),
                                              "Product_select": globals_wipPart1,
                                              "Header_list": Header_list,
                                              "data_list": data_list,
                                              "Label_list": Label_list,
                                              "DatasPlot1": DatasPlot1,
                                              "DatasPlot2": DatasPlot2,
                                              "DatasPlot3": DatasPlot3,
                                               "globals_loginuser": globals_loginuser})


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
    #print("Product_list2:" + " ".join(ProductList2))


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
        #return HttpResponse("Product_list count=0")
        return render(request, "runningtables.html", {"UDTime": UDTime,
                                                      "Type_list": GetTypesLists(),
                                                      "Type_select": globals_Type,
                                                      "Product_list": GetSelectTypeLists(globals_Type),
                                                      "Type_select2": globals_Type2,
                                                      "Product_list2": ProductList2})

    Header_list = GetHeaderList(bProduct, Product_list)
    data_list = GetDataList(globals_Type, globals_Wip, bProduct, Product_list)
    #print("Header_list:" + str(len(Header_list)) + ",data_list:" + str(len(data_list)))

    if(len(ProductList2) >0):
        bProduct2 = (models.Product.objects.filter(ProductID=globals_Part2).count() > 0)
        if (bProduct2):
            Product_list2 = LocalFunctions.GetProductList(globals_Type2)
        else:
            Product_list2 = LocalFunctions.GetPartList(globals_Type2, globals_Part2)
        if(len(Product_list2)>0):
            Header_list2 = GetHeaderList(bProduct2, Product_list2)
            data_list2 = GetDataList(globals_Type2, globals_Wip2, bProduct2, Product_list2)
            #print("Header_list2:" + str(len(Header_list2)) + ",data_list2:" + str(len(data_list2)))

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



    #print(data_list)
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

def GetSelectTypeListsAll(type):
    Product_list = []
    lstTemp = models.Titles.objects.filter(TypeID=type).values('Members')
    for t in lstTemp:
        strTemp = t["Members"]
        Product_list += [strTemp]
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