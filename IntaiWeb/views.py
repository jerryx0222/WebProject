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

    lstTypes = []
    lstProducts = []
    GetSelectLists(0,lstTypes, lstProducts)
    # print("Types:", lstTypes)
    # print("Products:", lstProducts)

    return render(request, "index.html", {"UDTime" : UDTime, "lstTypes" : lstTypes, "lstProducts" : lstProducts})


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

def outputers(request,GroupID='2ETC02'):
    #GroupID = request.GET.get('type')   #"2ETC02"
    if not GroupID:
        return HttpResponse("type require")

    Header_list=['日期', '產品', '輸出', '庫存', '比率', '差異']
    date_list = []
    data_list = []

    temp_list = models.Shiptable.objects.filter(TypeID=GroupID)
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
        temp_list = models.Shiptable.objects.filter(TypeID=GroupID, ShipDate=obj)
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



    return render(request, "outputers.html", {"Header_list" : Header_list, "data_list" : data_list, "UDTime" : UDTime})


def runningtables(request,tID='2ETC02'):
    #tID = request.GET.get('type')   #"2ETC02"
    pID = request.GET.get('part')    #"0244D02837P02"
    WipData = request.GET.get('wip')    #True


    if not tID:
        return HttpResponse("type require")
    print("TypeID:" + tID)
    if not pID:
        pID=""
    if not WipData:
        WipData=True
    else:
        WipData=False
    print("PartID:" + pID)
    if WipData:
        print("WipData:True")
    else:
        print("WipData:False")

    Header_list = []
    data_list = []

    #PartID="0244D02837P02"
    if (len(pID) <= 0):
        Product_list = LocalFunctions.GetProductList(tID)
    else:
        Product_list = LocalFunctions.GetPartList(tID, pID)

    if Product_list.count()<=0:
        return HttpResponse("Product_list count=0")

    if(len(pID)<=0):
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

    #print(Header_list)

    for obj in Product_list:
        hlist = []
        if (len(pID) <= 0):
            hlist += [obj.ProductID]
            temp_list = models.Product.objects.filter(ProductID=obj.ProductID)
        else:
            hlist += [obj.Members]
            temp_list = models.Part.objects.filter(PartID=obj.Members)

        for name in temp_list:
            hlist += [name.CName]
            break

        if (len(pID) <= 0):
            temp_list = models.runningtables.objects.filter(TypeID=tID, ProductID=obj.ProductID)
        else:
            temp_list = models.runningtables.objects.filter(GroupID=tID, ProductID=obj.Members)

        for v in reversed(temp_list):
            if WipData:
                hlist += [v.TargetCount]
            else:
                hlist += [v.WipCount]

        data_list += [hlist]

    SysDatas = models.SystemSet.objects.filter(DataName='UpdateDateTime')
    for obj in SysDatas:
        UDTime = obj.StrData

    return render(request, "runningtables.html", {"Header_list" : Header_list, "data_list" : data_list, "UDTime" : UDTime})


def GetSelectLists(lstTypes,lstProducts):
    lstTemp = models.Titles.objects.values('TypeID').order_by('TypeID').distinct()
    for t in lstTemp:
        strTemp = t["TypeID"]
        lstTypes += [strTemp]
        lstTemp2 = models.Titles.objects.filter(TypeID=strTemp).values('ProductID').order_by('ProductID').distinct()
        lstTemp3 = []
        for p in lstTemp2:
            lstTemp3 += [p["ProductID"]]
        lstProducts+=[lstTemp3]

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