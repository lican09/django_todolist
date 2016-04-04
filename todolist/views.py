# -*- coding: utf-8-*-
import logging
from django.shortcuts import render, redirect, resolve_url
from models import Item, UserProfile
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from forms import RegForm, LoginForm, EditPassForm
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
            print "from IP:", get_client_ip(request)
            print request.user, "Logined"
            return redirect("/index/")
        else:
            # 验证失败
            return HttpResponse(u"验证失败")
    return render(request, "login.html", locals())


# 注销
def do_logout(request):
    logout(request)
    return redirect("/login/")


# 待办事项列表,需要对列表进行分页
@login_required(login_url="/login/")
def index(request):
    try:
        user_id = UserProfile.objects.get(email=request.user)
        item_list = Item.objects.filter(user=user_id).order_by("-pub_date")
        paginator = Paginator(item_list, 5)
        try:
            page = int(request.GET.get("page", 1))
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
            obj = Item.objects.create(content=content, user=user_id)
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


#  标记事项完成
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


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            print "POST do_reg"
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = UserProfile.objects.create(
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),
                                    reg_ip=get_client_ip(request))
                user.save()

                # 登录
                print "OK reg_form"
                print reg_form.cleaned_data["email"], reg_form.cleaned_data["password"]
                user = authenticate(username=reg_form.cleaned_data["email"], password=reg_form.cleaned_data["password"])
                login(request, user)
                return redirect("/index/")
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 警告页面
def warning(request):
    return render(request, "warning.html", locals())


# 记录客户端注册的IP地址
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


# 修改密码
@login_required(login_url="/login/")
def edit_pass(request):
    email = request.user.email
    if request.method == 'POST':
        edit_form = EditPassForm(request.POST)
        print str(edit_form)
        if edit_form.is_valid():
            pass1 = edit_form.cleaned_data["password"]
            pass2 = edit_form.cleaned_data["password2"]
            # 更改密码
            if pass1 == pass2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(edit_form.cleaned_data["password"])
                user.save()
                # 更改成功
                user = authenticate(username=email, password=pass1)
                login(request, user)
            else:
                return redirect("/edit_pass/")
            return redirect("/index/")
        else:
            return render(request, 'failure.html', {'reason': edit_form.errors})
    else:
        edit_form = EditPassForm()
    return render(request, 'modify_pass.html', locals())
