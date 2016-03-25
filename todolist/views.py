# -*- coding: utf-8-*-
import logging
from django.shortcuts import render, redirect, resolve_url
from models import Item,UserProfile
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from forms import RegForm,LoginForm
from django.contrib.auth.hashers import make_password
# Create your views here.
logger = logging.getLogger('todolist.views')

# 登录认证
def do_login(request):
    if request.method == "POST":
        print "POST login"
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(username=email, password=password)
        if user:
            # 验证通过
            login(request, user)
            return redirect("/index/")
        else:
            # 验证失败
            return HttpResponse(u"验证失败")
    return render(request, "login.html", locals())

def do_logout(request):
    logout(request)
    return redirect("/login/")


# 待办事项列表,需要对列表进行分页
@login_required(login_url="/login/")
def index(request):
    print type(get_client_ip(request)),get_client_ip(request)
    print request.user
    try:
        user_id = UserProfile.objects.get(email=request.user)
        item_list = Item.objects.filter(user=user_id).order_by("-pub_date")
        paginator = Paginator(item_list, 5)
        try:
            page = int(request.GET.get("page",1))
            item_list = paginator.page(page)
        except (PageNotAnInteger, InvalidPage, EmptyPage):
            item_list = paginator.page(1)
    except Exception as e:
        print e
    return render(request, "index.html", locals())

# 增加待办事项
@login_required(login_url="/login/")
def add(request):
    content = request.GET.get("item", None)
    if not content:
        return redirect(resolve_url("index"))
    try:
        user_id = UserProfile.objects.get(email=request.user)
        if len(content) > 0:
            obj = Item.objects.create(content=content,user=user_id)
            if obj:
                return redirect(resolve_url("index"))
    except Exception as e:
        print e
        return render(request, "message.html", {"message": u"待办事项添加失败"})

# 修改待办事项
@login_required(login_url="/login/")
def edit(request):
    try:
        item_id = request.GET.get("item_id", None)
        content = request.GET.get("item", None)
        if len(item_id) > 0 and len(content) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.content = content
            obj.save()
        return redirect("/index/")
    except Exception as e:
        print e
    return render(request, "message.html", {"message": u"待办事项修改失败"})

# 删除待办事项
@login_required(login_url="/login/")
def delete(request):
    try:
        item_id = request.GET.get("item_id", None)
        if len(item_id) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.delete()
        return redirect("/index/")
    except Exception as e:
        print e
    return render(request, "message.html", {"message": u"待办事项删除失败"})

# 标记事项完成
@login_required(login_url="/login/")
def done(request):
    try:
        item_id = request.GET.get("item_id", None)
        if len(item_id) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.is_done = False if obj.is_done else True
            # if obj.is_done:
            #     obj.is_done = False
            # else:
            #     obj.is_done = True
            obj.save()
        return redirect("/index/")
    except Exception as e:
        print e
    return render(request, "message.html", {"message": u"待办事项状态修改失败"})


def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = UserProfile.objects.create(
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),
                                    reg_ip=get_client_ip(request))
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect("/index/")
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())



def warning(request):
    return render(request, "warning.html", locals())

def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip