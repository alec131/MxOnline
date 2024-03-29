# *_* coding:utf-8 *_*
#视图导入html文本渲染模块
from django.shortcuts import render
#视图导入通用视图
from django.views.generic import View
#视图导入模型，对数据进行获取及逻辑处理
from .models import CourseOrg, CityDict, Teacher
#导入分页功能
from pure_pagination import Paginator, PageNotAnInteger
#视图导入model_form，对表单进行校验逻辑处理
from .forms import UserAskForm
#视图导入http响应模块
from django.http import HttpResponse
from operation.models import UserFavorite
from courses.models import Course
from django.db.models import Q
# Create your views here.

# 定义OrgView类，继承View统一视图
class OrgView(View):
    """
    课程机构功能
    """
    def get(self, request):
        #获取所有课程机构，all_orgs是模型类CourseOrg(数据表)通过QuerySet查询产生的一个实例，
        all_orgs = CourseOrg.objects.all()
        #热门机构排名，order_by是QuerySet类方法
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #取出机构所有城市
        all_citys = CityDict.objects.all()

        # 授课机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        #取出筛选城市,关键字'city'和html里拼接的路径要一致
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        #取出机构类别筛选，同上
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        #学习人数排名筛选，同上
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                # 数字大小从大到小排序
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
                # 输出排序后的课程机构数量
        org_nums = all_orgs.count()

        #课程机构分页
        try:
            # 获取当前页，这里设置为首页
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            #调用分页类，all_orgs的值来自前面过滤操作后的一个值，指定分页策略
        p = Paginator(all_orgs, 3, request=request)
        # 调用page函数进行分页
        orgs = p.page(page)
        # 调用render函数返回org列表页面
        return render(request, "org-list.html", {
            # 页面传入参数
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })

class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html', {
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgDescView(View):
    '''
    机构课程详情页
    '''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })

class OrgTeacherView(View):
    '''
    机构教师页
    '''
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class AddFavView(View):
    '''
    用户收藏，用户取消收藏
    '''
    def post (self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0 :
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 授课机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords)|Q(work_position__icontains=search_keywords))
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")
        sorted_teachers = Teacher.objects.all().order_by("click_nums")[:3]

        # 讲师分页
        try:
            # 获取当前页，这里设置为首页
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 调用分页类，all_teachers的值来自前面过滤操作后的一个值，指定分页策略
        p = Paginator(all_teachers, 10, request=request)
        # 调用page函数进行分页
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers":teachers,
            "sorted_teachers":sorted_teachers,
        })

class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav = True
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True
        # 讲师排行
        sorted_teachers = Teacher.objects.all().order_by("click_nums")[:3]
        return render(request, "teacher-detail.html", {
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teachers':sorted_teachers,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav,
        })
