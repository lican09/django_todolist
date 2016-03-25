#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
import re

class CheckBrower(object):
    def process_request(self, request):
        agent = request.META['HTTP_USER_AGENT']
        result = re.findall("MSIE [5678]", agent)
        path=request.META['PATH_INFO']
        if len(result) > 0:
            # 就应该显示浏览器升级的页面
            # return render(request, "warning.html")
            path = request.META['PATH_INFO']
            if path.find("/warning") == -1:
                return redirect("/warning/")