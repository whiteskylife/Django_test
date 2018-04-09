from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class Row1(MiddlewareMixin):                # 必须要继承 MiddlewareMixin
    def process_request(self, request):
        print('Row1------')

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):   #
        """
        :param request:
        :param view_func: 视图函数
        :param view_func_args: 视图函数的参数,urls中定义的(\d+): url(r'^test/(\d+)$', views.test)
        :param view_func_kwargs:视图函数的参数,urls中定义的(?p<nid>\d+): url(r'^test/(?P<nid>\d+)$', views.test)
        :return:
        """
        print('Row1_process_view')

    def process_response(self, request, response):
        print('R1 response')
        return response


class Row2(MiddlewareMixin):
    def process_request(self, request):
        print('Row2------')
        # return HttpResponse('走')        # 这里return后，jango1.10版本以后，不会再走row3中的两个方法，直接返回；在jango1.8/1.7中会从row3开始返回

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        print('Row2_process_view')

    def process_response(self, request, response):
        print('R2 response')
        return response


class Row3(MiddlewareMixin):
    def process_request(self, request):
        print('Row3------')

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        print('Row3_process_view')

    def process_response(self, request, response):
        print('R3 response')
        return response

    def process_exception(self, request, exception):
        '''
         :param request:
         :param exception:异常信息
         :return:
        '''
        if isinstance(exception,ValueError):
            return HttpResponse('出现异常》。。')

    def process_template_response(self,request,response):
        # 如果Views中的函数返回的对象中，具有render方法
        print('-----------------------')
        return response