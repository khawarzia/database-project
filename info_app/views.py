from django.shortcuts import render,redirect
from .models import department,course,sections_offered,result
from profile_app.models import profile,time_slots
from datetime import datetime

static_slot_times = ['8','9','10','11','12','1','2','3','4']

def preferneces(request):
    template = 'info/preference.html'
    context = {}
    profile_obj = profile.objects.get(user=request.user)
    if request.method == 'POST':
        if static_slot_times.index(request.POST['from']) < static_slot_times.index(request.POST['to']):
            try:
                obj = time_slots.objects.get(start_time=int(request.POST['from']),end_time=int(request.POST['to']))
                profile_obj.preferred_slots.add(obj)
                profile_obj.save()
            except:
                obj = time_slots()
                obj.start_time = int(request.POST['from'])
                obj.end_time = int(request.POST['to'])
                obj.save()
                profile_obj.preferred_slots.add(obj)
                profile_obj.save()
            context['message'] = 'Preference has been added'
        else:
            context['message'] = 'Start time cannot be same as or after End time'
    context['profile'] = profile_obj
    return render(request,template,context)

def delete_preference(request,id):
    profile_obj = profile.objects.get(user=request.user)
    time_obj = time_slots.objects.get(pk=id)
    try:
        profile_obj.preferred_slots.remove(time_obj)
        profile_obj.save()
    except:
        pass
    return redirect('/preference')

def select_subjects(request,**kwargs):
    template = 'info/subjects.html'
    context = {}
    profile_obj = profile.objects.get(user=request.user)
    sections_available = sections_offered.objects.filter(
        for_course__from_department=profile_obj.department_name,
        for_course__for_semester=profile_obj.from_semester,
        for_course__for_session=profile_obj.from_session,
        for_course__for_semester_year=str(datetime.now().year)
    )
    context['data'] = sections_available
    try:
        context['message'] = kwargs.get('message')
    except:
        pass
    context['profile'] = profile_obj
    return render(request,template,context)

def register_subject(request,id,section_name):
    section_objs = sections_offered.objects.filter(for_course__id=id)
    for i in section_objs:
        if request.user in i.students.all():
            return select_subjects(request,message='Already registered this subject in Section '+i.name)
    for i in section_objs:
        if i.name == section_name:
            if i.students.count() < i.for_course.section_capacity:
                i.students.add(request.user)
                i.save()
            else:
                return select_subjects(request,message='Capacity for this section has been reached. Please register in any other section.')
    return redirect('/select-subjects')

def unregister_subject(request,id):
    section_obj = sections_offered.objects.get(pk=id)
    section_obj.students.remove(request.user)
    section_obj.save()
    return redirect('/select-subjects')

def result_sheet(request):
    template = 'info/result.html'
    context = {}
    context['data'] = result.objects.filter(user=request.user)
    context['profile'] = profile.objects.get(user=request.user)
    return render(request,template,context)