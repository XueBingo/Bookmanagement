#coding：utf-8
from django.shortcuts import render
from django.http import HttpResponse
from bookmanageapp import models
import hashlib
import datetime
from django.db.models import Sum
import decimal

#encode the passcode
def getPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

#initialize the database
def hello(request):
    data = models.Userinfo(NO = 0, username = 'master', password = getPassword('master'), name = 'master', age = 22, gender = 'Male', )
    data.save()
    data = models.Userinfo(NO = 1, username = 'john', password = getPassword('john'), name = 'john', age = 24, gender = 'Male', )
    data.save()
    data = models.Userinfo(NO = 0, username = 'kevin', password = getPassword('kevin'), name = 'john', age = 25 , gender = 'Male', )
    data.save()
    data = models.Account(NO = 0, credit = 100000)
    data.save()
    return HttpResponse("Initialized!")

#generated NO automatically
def Ordernumber():
    last = models.Order.objects.all().order_by('NO').last()
    if not last:
        return 1
    return last.NO+1

def Accountnumber():
    last = models.Account.objects.all().order_by('NO').last()
    if not last:
        return 1
    return last.NO+1

def Book_infonumber():
    last = models.Book_info.objects.all().order_by('NO').last()
    if not last:
        return 1
    return last.NO+1

def Userinfonumber():
    last = models.Userinfo.objects.all().order_by('NO').last()
    if not last:
        return 1
    return last.NO+1

#the login function
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = getPassword(request.POST.get('password'))
        if not all([username, password]):
            return HttpResponse('Invalid username or password!')
        else:
            user = models.Userinfo.objects.filter(username=username, password=password)
            if len(user):
                request.session['user'] = {
                    'NO': user[0].NO,
                    'username': username,
                    'password': password
                }
                context = {
                    'status': username,
                    'aa': 'online',
                    'lenght': 1
                }
                return render(request, 'index.html', context)

            else:
                context = {
                    'aa': 'Invalid username or password!'
                }
                return render(request, 'login.html', context)
    else:
        context = {
            'status': 'guest',
            'length': 0
        }
        return render(request, 'login.html', context)

def index(request):
    try:
        user_information = request.session['user']
        username = user_information['username']
    except:
        context = {
            'status': 'guest',
        }
        return render(request, 'index.html', context)
    else:
        context = {
            'status': username,
            'lenght': 1,
        }
    return render(request, 'index.html', context)

def logout(request):
    try:
        del request.session['user']
    except:
        message = 'unlogged'
        return HttpResponse(message)
    else:
        return render(request, 'index.html')

def showallusers(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'showallusers.html', context)
    if _id == 0:
        users = models.Userinfo.objects.all()
    else:
        users = models.Userinfo.objects.filter(NO=_id)
    return render(request, 'showallusers.html', {'users': users})

def insertuser(request):
    if request.method == "POST":
        try:
            user_information = request.session['user']
            _id = user_information['NO']
        except:
            context = {
                'not_login': True,
                'msg': False,
            }
            return render(request, 'insertuser.html', context)
        if _id == 0:
            username = request.POST.get('user_username')
            name = request.POST.get('user_name')
            password = request.POST.get('user_password')
            gender = request.POST.get('user_gender')
            age = request.POST.get('user_age')
            if not all([username, password, gender, age]):
                context = {
                    'msg': 'Lack of Parameters',
                }
                return render(request, 'insertuser.html', context)
            user = models.Userinfo.objects.filter(username=username)
            if len(user):
                context = {
                    'msg': 'Username occupied!',
                }
                return render(request, 'insertuser.html', context)
            data = models.Userinfo()
            data.NO = Userinfonumber()
            data.name = name
            data.username = username
            data.password = getPassword(password)
            data.gender = gender
            data.age = age
            data.save()
            context = {
                'sucess': 'successful insertion',
            }
            return render(request, 'insertuser.html', context)
        else:
            context = {
                'error': 'Not previliged'
            }
            return render(request, 'insertuser.html', context)
    else:
        return render(request, 'insertuser.html')

def updateuserinfo(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
        currentuser = user_information['username']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'updateuserinfo.html', context)
    context = {
        'msg': 'enter your infomation'
    }
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        user = models.Userinfo.objects.filter(username=username)
        if len(user) and currentuser != username:
            context = {
                'msg': 'You cannot change others\' info!',
            }
            return render(request, 'updateuserinfo.html', context)
        models.Userinfo.objects.filter(NO=_id).update(name=name, username=username, password=getPassword(password), gender=gender, age=age)
        context = {
            'msg': 'successful updation'
        }
        return render(request, 'updateuserinfo.html', context)
    else:
        return render(request, 'updateuserinfo.html', context)

def searchbook(request):
    if request.method == "POST":
        try:
            user_information = request.session['user']
            _id = user_information['NO']
        except:
            context = {
                'not_login': True,
                'msg': False,
            }
            return render(request, 'searchbook.html', context)
        NO = request.POST.get('NO')
        ISBN = request.POST.get('ISBN')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        data = models.Book_info.objects.filter(NO__contains=NO, ISBN__contains=ISBN, title__contains=title, author__contains=author, publisher__contains=publisher,)
        context = {
            'data': data,
            'msg': True
        }
        return render(request, 'searchbook.html', context)
    else:
        context = {
            'msg': False,
        }
        return render(request, 'searchbook.html', context)

def updatebookinfo(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
    except:
        context = {
            'not_login': True,
            'msg': False,
        }
        return render(request, 'updatebookinfo.html', context)
    context = {
            'msg': 'enter the infomation'
        }
    if request.method == "POST":
        ISBN = request.POST.get('ISBN')
        title = request.POST.get('title')
        NO = request.POST.get('NO')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        price = request.POST.get('price')
        if not all([ISBN, NO, title, author, publisher]):
            context = {
                'msg': 'Lack of Parameters!'
            }
            return render(request, 'updatebookinfo.html', context)
        #To do: make sure the ISBN is unique
        models.Book_info.objects.filter(NO=NO).update(ISBN=ISBN, title=title, author=author, publisher=publisher)
        models.Sale.objects.filter(NO=NO).update(price=price)
        context = {
            'msg': 'successful updation'
        }
        return render(request, 'updatebookinfo.html', context)
    else:
        return render(request, 'updatebookinfo.html', context)

def orderbook(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
        currentuser = user_information['username']
    except:
        context = {
            'not_login': True,
            'msg': False,
        }
        return render(request, 'orderbook.html', context)
    if request.method == "POST":
        NO = Ordernumber()

        ISBN = request.POST.get('ISBN')
        amount = request.POST.get('cost')
        number = request.POST.get('number')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')

        if not all([ISBN, amount, number]):
            context = {
                'msg': 'Missing infomation',
            }
            return render(request, 'orderbook.html', context)

        obj = models.Book_info.objects.filter(ISBN=ISBN)
        if not len(obj):
            bookdata = models.Book_info()
            bookdata.ISBN = ISBN
            bookdata.NO = Book_infonumber()
            bookdata.title = title
            bookdata.author = author
            bookdata.publisher = publisher
            bookdata.save()
            context = {
                'sucess': 'new book, successful order',
            }
        else:       
            context = {
                'sucess': 'old book, successful order',
            }
        data = models.Order()
        data.NO = Ordernumber()
        data.Book_NO = models.Book_info.objects.get(ISBN=ISBN)
        data.amount = amount
        data.date = datetime.date.today()
        data.number = number
        data.status = 'Unpaid'
        data.user_NO = models.Userinfo.objects.get(NO=_id)
        data.save()     
        return render(request, 'orderbook.html', context)
            
    else:
        return render(request, 'orderbook.html')

def purchaseorder(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'purchaseorder.html', context)
    unpaidorders = models.Order.objects.filter(status='Unpaid')
    return render(request, 'purchaseorder.html', {'unpaidorders': unpaidorders})     

def pay(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
        currentuser = user_information['username']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'purchaseorder.html', context)
    amount = request.GET.get('amount')
    credit = models.Account.objects.all().order_by('NO').last().credit
    if decimal.Decimal(amount) > credit:
        context = {
            'msg': 'out of Money!'
        }
        return render(request, 'purchaseorder.html', context)

    NO = request.GET.get('NO')
    models.Order.objects.filter(NO=NO).update(status='Paid', user_NO=_id, date=datetime.date.today())
    context = {
        'sucess': 'successful payment! There is ' + str(credit-decimal.Decimal(amount)) + 'on account'
    }
    acdata  = models.Account()
    acdata.NO = Accountnumber()
    acdata.credit = credit-decimal.Decimal(amount)
    acdata.save()
    return render(request, 'purchaseorder.html', context)

def returnorder(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
        currentuser = user_information['username']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'purchaseorder.html', context)
    NO = request.GET.get('NO')
    models.Order.objects.filter(NO=NO).update(status='Returned', user_NO=_id, date=datetime.date.today())
    context = {
        'sucess': 'successful return',
    }
    return render(request, 'purchaseorder.html', context)

def addstock(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'addstock.html', context)
    context = {
            'msg': 'enter the infomation'
        }
    if request.method == "POST":
        NO = request.POST.get('NO')
        add = int(request.POST.get('addstock'))
        obj = models.Sale.objects.filter(NO=NO)
        if len(obj):
            origstock = obj[0].stock
            models.Sale.objects.filter(NO=NO).update(stock=origstock+add)
        else:
            data = models.Sale()
            data.stock = add
            data.price = 999
            data.NO = models.Book_info.objects.get(NO=NO)
            data.save()
        context = {
            'msg': 'successful updation'
        }
        return render(request, 'addstock.html', context)
    else:
        return render(request, 'addstock.html', context)

def sellbook(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
        currentuser = user_information['username']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'sellbook.html', context)
    context = {
            'msg': 'enter the infomation'
        }
    if request.method == "POST":
        NO = request.POST.get('NO')
        number = int(request.POST.get('number'))
        origstock = models.Sale.objects.get(NO=NO).stock
        if number > origstock:
            context = {
                'msg': 'out of Stock!'
            }
            return render(request, 'sellbook.html', context)
        price = models.Sale.objects.get(NO=NO).price
        models.Sale.objects.filter(NO=NO).update(stock=origstock-number)
        context = {
            'msg': 'Good job! there is ' + str(origstock-number) + ' in stock'
        }
        data = models.Order()
        data.NO = Ordernumber()
        data.Book_NO = models.Book_info.objects.get(NO=NO)
        data.status = 'Sale'
        data.number = number
        data.user_NO = models.Userinfo.objects.get(NO=_id)
        data.date = datetime.date.today()
        data.amount = price * number
        data.save()
        acdata = models.Account()
        acdata.NO = Accountnumber()
        acdata.credit = models.Account.objects.all().order_by('NO').last().credit + price * number
        acdata.save()
        return render(request, 'sellbook.html', context)
    else:
        return render(request, 'sellbook.html', context)

def checkrecord(request):
    try:
        user_information = request.session['user']
        _id = user_information['NO']
    except:
        context = {
            'not_login': True,
        }
        return render(request, 'checkrecord.html', context)
    if request.method == "POST":
        datefrom = request.POST.get('datefrom')
        dateto   = request.POST.get('dateto')
        data = models.Order.objects.filter(date__lte=dateto, date__gt=datefrom,)
        context = {
            'data': data,
            'msg': True
        }
        return render(request, 'checkrecord.html', context)
    else:
        context = {
            'msg': False,
        }
        return render(request, 'checkrecord.html', context)

def salesorder(request):
    booksales = models.Order.objects.filter(status='Sale').values("Book_NO").annotate(sales_sum=Sum("number")).values('Book_NO', 'Book_NO__title', 'sales_sum').order_by('-sales_sum')
    # orders = models.Order.objects.all()
    # print(booksales)
    # print(orders)
    return render(request, 'showbook.html', {'booksales': booksales})
