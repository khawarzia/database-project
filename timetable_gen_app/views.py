from django.shortcuts import render
from info_app.models import department,course,sections_offered,profile
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from .resource import get_pref_slots,get_ordered_courses,check_or_get_series,check_empty_and_fill

static_series_time_1 = ['89','910','1011','1112','12','23','34']
static_series_time_2 = ['89','910','1011','12','23']
static_series_time_3 = ['89','910','12']

monday = {'89':'','910':'','1011':'','1112':'','121':'','12':'','23':'','34':''}
tuesday = {'89':'','910':'','1011':'','1112':'','121':'','12':'','23':'','34':''}
wednesday = {'89':'','910':'','1011':'','1112':'','121':'','12':'','23':'','34':''}
thursday = {'89':'','910':'','1011':'','1112':'','121':'','12':'','23':'','34':''}
friday = {'89':'','910':'','1011':'','1112':'','121':'','12':' ','23':'','34':''}

def generate_timetables(request):
    template = 'time/timetables.html'
    sel_department = request.POST['department']
    sel_session = request.POST['session']
    sel_semester = request.POST['semester'].split(' ')[0]
    sel_semester_year = request.POST['semester'].split(' ')[1]
    context = {
        'profile':profile.objects.get(user=request.user),
        'department':sel_department,
        'session':sel_session,
        'semester':request.POST['semester']
    }
    
    selected_sections = sections_offered.objects.filter(
        for_course__from_department__name=sel_department,
        for_course__for_semester=sel_semester,
        for_course__for_semester_year=sel_semester_year,
        for_course__for_session=sel_session
    )

    sections_dict = {}
    sections_course_lists = {}

    for i in selected_sections:
        sections_course_lists[i.name] = []
        temp_dict = {'course':i.for_course.name,'teacher':i.for_course.taught_by}
        if i.for_course.contact_hour == 3:
            if i.for_course.credit_hour == 1:
                temp_dict['class'] = [3]
            else:
                temp_dict['class'] = [2,1]
        else:
            temp_dict['class'] = [i.for_course.contact_hour]
        try:
            sections_dict[i.name].append(temp_dict)
        except:
            sections_dict[i.name] = [temp_dict]

    for i in sections_dict:
        for j in sections_dict[i]:
            sections_course_lists[i].append(j['course'])

    teacher_pref = {}
    for i,j in sections_dict.items():
        for k in j:
            temp = profile.objects.get(user__username=k['teacher'].username)
            teacher_pref[temp.user] = get_pref_slots(temp.preferred_slots.all()) 
        break

    final_result = {}
    for i,j in sections_dict.items():
        final_result[i] = {'monday':dict(monday),'tuesday':dict(tuesday),'wednesday':dict(wednesday),'thursday':dict(thursday),'friday':dict(friday)}

    for i,j in final_result.items():
        for k in get_ordered_courses(sections_dict[i]):
            pref_slots = teacher_pref[k['teacher']]
            for l in k['class']:
                temp = check_or_get_series(pref_slots,l)
                if len(temp) != 0:
                    final_result = check_empty_and_fill(final_result,temp,l,k['course'],sections_course_lists)
        break
                
    context['final_result'] = final_result
    return render(request,template,context)



def departments_list(request):
    temp_list = []
    for i in department.objects.all():
        temp_list.append(i.name)
    return JsonResponse(temp_list,safe=False)

def sessions_list(request):
    sel_year = int(datetime.now().year) - 4
    temp_list = []
    for i in range(5):
        temp_list.append(sel_year+i)
    return JsonResponse(temp_list,safe=False)

def semesters_list(request):
    sel_year = str(datetime.now().year)
    temp_list = ['Fall '+sel_year,'Spring '+sel_year]
    return JsonResponse(temp_list,safe=False)