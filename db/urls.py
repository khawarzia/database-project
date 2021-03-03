"""db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from info_app import views as info_view
from profile_app import views as profile_view
from timetable_gen_app import views as time_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',profile_view.home,name='home'),
    path('login',profile_view.login,name='login'),
    path('logout',profile_view.logout,name='logout'),

    path('preference',info_view.preferneces,name='preference'),
    path('delete-preference/<int:id>',info_view.delete_preference,name='delete-preference'),

    path('select-subjects',info_view.select_subjects,name='select-subjects'),
    path('register-subject/<int:id>/<str:section_name>',info_view.register_subject,name='register-subject'),
    path('unregister-subject/<int:id>',info_view.unregister_subject,name='unregister-subject'),

    path('result-sheet',info_view.result_sheet,name='result-sheet'),

    path('generate-timetables',time_view.generate_timetables,name='generate-timetables'),

    path('departments',time_view.departments_list,name='departments-list'),
    path('sessions',time_view.sessions_list,name='sessions-list'),
    path('semesters',time_view.semesters_list,name='semesters-list'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)