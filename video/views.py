from .models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import re

# Create your views here.


def index(request):
    # 获取视频分类作为菜单数据
    menu_list = Cate.objects.all()
    # 返回最热的4条数据
    hot_list = Video.objects.all().order_by('-views')[:4]
    # 返回迅雷电影资源的最新4条数据
    analysis_list_1 = Video.objects.filter(cate=Cate.objects.get(name='迅雷电影资源')).order_by('-create_time')[:4]
    # 返回迅雷电影资源的最新4条数据
    analysis_list_2 = Video.objects.filter(cate=Cate.objects.get(name='迅雷电影资源')).order_by('-create_time')[4:8]
    # 返回迅雷电影资源的最新4条数据
    analysis_list_3 = Video.objects.filter(cate=Cate.objects.get(name='迅雷电影资源')).order_by('-create_time')[8:12]
    # 返回经典影片的最新4条数据
    classics_list = Video.objects.filter(cate=Cate.objects.get(name='经典影片')).order_by('-create_time')[:4]
    return render(request, 'index.html', locals())


# 视频详情页
def videoDetail(request,vid):
    # 获取视频分类作为菜单数据
    menu_list = Cate.objects.all()
    # 获取视频数据
    id = int(vid)
    video = Video.objects.get(id=vid)
    # 获取视频专辑
    try:
        set_name = Set.objects.get(video=id).name
        video_set = Set.objects.filter(name=set_name)
    except:
        random_video = Video.objects.order_by('?')[:5]
    # 增加访问人数
    try:
        video.views += 1
        video.save()
    except Exception as e:
        print(e)

    # 获取点赞人数
    try:
        likes = Likes.objects.filter(video=video).count()
    except:
        likes = 0

    # 添加观看记录
    try:
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            history = History.objects.create(user=user,video=video)
            history.save()
    except Exception as e:
        print(e)

    return render(request, 'single.html', locals())


# 观看历史页
# @login_required()
def viewHistory(request):
    # 获取视频分类作为菜单数据
    menu_list = Cate.objects.all()
    try:
        # 获取用户
        user = User.objects.get(username=request.user.username)
        # 获取用户的观看历史记录
        history_list = History.objects.filter(user=user)
    except Exception as e:
        return redirect('/login')
    # 分页
    cate_video_list = getPage(request,history_list)
    return render(request,'history.html',locals())


# 分页代码
def getPage(request, video_list):
    paginator = Paginator(video_list, 12)
    try:
        page = int(request.GET.get('page', 1))
        video_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        video_list = paginator.page(1)
    return video_list


# 视频分类页
def videoCate(request,cateid):
    # 获取视频分类作为菜单数据
    menu_list = Cate.objects.all()
    # 获取分类视频
    catename = Cate.objects.get(id=cateid)
    video_list = Video.objects.filter(cate = catename)
    # 分页
    cate_video_list = getPage(request,video_list)
    return render(request,'cate.html',locals())


# 登录页面
def logIn(request):
    # 判断是否已经登录
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        if request.method == 'GET':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return render(request, 'login.html', locals())
        elif request.method == 'POST':
            username = request.POST.get("username", '')
            password = request.POST.get("password", '')
            if username != '' and password != '':
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(request.session['login_from'])
                else:
                    errormsg = '用户名或密码错误！'
                    return render(request, 'login.html', locals())
            else:
                return JsonResponse({"e": "chucuo"})


# 注册页面
def register(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'register.html',locals())
    elif request.method == 'POST':
        # 接收表单数据
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        email = request.POST.get("email", '')
        checkcode = request.POST.get("check_code", '')

        result_name = re.compile(r"[a-zA-Z\u4e00-\u9fa5]{4,6}")
        result_paswd = re.compile(r"^[a-zA-Z]\w{6,8}")
        # 判断文本框是否为空
        if username != '' and password != '' and checkcode != '':
            # 判断用户和密码是否符合格式
            if result_name.match(username) and result_paswd.match(password):
                # 判断验证码是否正确
                if checkcode == request.session['CheckCode'].lower():
                    # 判断用户是否存在
                    if User.objects.filter(username=username).exists() == False:
                        # 注册
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        # 登录
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        # 重定向跳转
                        return redirect(request.session['login_from'], '/')

                else:
                    errormsg = '验证码错误！'
                    # return render(request, 'register.html', locals())
            else:
                errormsg = '用户名或密码格式错误！'
                # return render(request, 'register.html', locals())
        else:
            errormsg = '不能为空！！'

    return render(request, 'register.html', locals())

# 注销
def logOut(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])


# 视频点赞功能
# @login_required
def like(request):
    if request.method == 'POST':
        videoid = request.POST.get("vid")
        video = Video.objects.get(id=videoid)
        user = request.user
        try:
            Likes.objects.get_or_create(
                    user=user,
                    video=video,
                )
            likes = Likes.objects.filter(video=video).count()
            return JsonResponse({"success": True,"lik": likes})
        except Exception as e:
            return JsonResponse({"success": False})

    else:
        return JsonResponse({"success": False})


# 验证码
def check_code(request):
    import io
    from .import check_code as CheckCode

    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())


# 搜索功能
def search(request):
    menu_list = Cate.objects.all()
    if request.method == 'POST':
        search_name = request.POST.get('search')
        search_list = Video.objects.filter(name__icontains=search_name)
        return render(request, 'search.html', locals())


