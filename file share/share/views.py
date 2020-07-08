import random
import string
import datetime
import json
from .forms import RegisterForm
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponsePermanentRedirect, FileResponse

from .models import Upload


class IndexView(TemplateView):
    template_name = 'index.html'
    def index(self,request):
        return render(request,'index.html')

class HomeView(TemplateView):
    '''用来展示主页的视图类
    '''
    template_name = 'base.html'

    def post(self, request):
        # 如果表单中有文件
        if request.FILES:
            file = request.FILES.get('file')
            name = file.name
            size = int(file.size)
            path = 'myproject/static/file/' + name
            with open(path, 'wb') as f:
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8))
            uname = str(request.user.username)
            upload = Upload(
                path=path,
                name=name,
                filesize=size,
                code=code,
                uname=uname
            )
            upload.save()
            return HttpResponsePermanentRedirect("/s/" + code)

class RegisterView(TemplateView):

    template_name = 'register.html'
    form = RegisterForm()

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/index')
        return render(request,'register.html',context={'form':form})

class DisplayView(ListView):
    '''展示文件的视图类
    '''
    def get(self, request, code):
        uploads = Upload.objects.filter(code=code)
        if uploads:
            for upload in uploads:
                upload.downloadcount += 1
                upload.save()
        return render(request, 'content.html', {'content': uploads, 'host': request.get_host()})


class MyView(ListView):
    '''用户管理视图类，就是用户管理文件的那个页面的视图类
    '''

    def get(self, request):
        uid = request.user.username
        uploads = Upload.objects.filter(uname=uid)
        for upload in uploads:
            upload.downloadcount += 1
            upload.save()
        return render(request, 'content.html', {'content': uploads})

    def post(self, request):
        # 如果表单中有文件
        if request.FILES:
            file = request.FILES.get('file')
            name = file.name
            size = int(file.size)
            path = 'myproject/static/file/' + name
            with open(path, 'wb') as f:
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8))
            uname = str(request.user.username)
            print(uname)
            upload = Upload(
                path=path,
                name=name,
                filesize=size,
                code=code,
                uname=uname
            )
            upload.save()
            return HttpResponsePermanentRedirect("/s/" + code)

class SearchView(ListView):
    '''搜索功能的视图类
    '''

    def get(self, request):
        code = request.GET.get('kw')
        u = Upload.objects.filter(name__icontains=str(code))
        data = {}
        if u :
            # 将符合条件的数据放到 data 中
            for i in range(len(u)):
                u[i].downloadcount += 1
                u[i].save()
                data[i]={}
                data[i]['download'] = u[i].downloadcount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['size'] = u[i].filesize
                data[i]['time'] = str(u[i].datetime.strftime('%Y-%m-%d %H:%M'))
                # 时间格式化
                data[i]['key'] = u[i].code
        # django 使用 HttpResponse 返回 json 的标准方式，content_type 是标准写法
        return HttpResponse(json.dumps(data), content_type="application/json")

def down_file(request,code):
    file_info = Upload.objects.get(code=code)
    file = open(file_info.path,'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment;filename="%s"' % file_info.name
    return response