from random import shuffle

static_slot_times = ['8','9','10','11','12','1','2','3','4']

def get_pref_slots(a):
    retval = []
    for i in a:
        st = static_slot_times.index(str(i.start_time))
        en = static_slot_times.index(str(i.end_time))
        if (en - st) == 1:
            retval.append('{}{}'.format(i.start_time,i.end_time))
        else:
            for j in range(en-st):
                retval.append(static_slot_times[st+j]+static_slot_times[st+j+1])
    return retval

def get_ordered_courses(a):
    retval = []
    shuffle(a)
    for i in a:
        if i['class'] == [3]:
            retval.append(i)
    for i in a:
        if i['class'] == [2]:
            retval.append(i)
    for i in a:
        if i['class'] == [1]:
            retval.append(i)
    for i in a:
        if i['class'] == [2,1]:
            retval.append(i)
    return retval

static_series_time_1 = ['89','910','1011','1112','12','23','34']
static_series_time_2 = ['89','910','1011','12','23']
static_series_time_3 = ['89','910','12']

def check_or_get_series(a,b):
    if b == 3:
        temp = set(set(static_series_time_3) & set(a)).union(static_series_time_3)
    elif b == 2:
        temp = set(set(static_series_time_2) & set(a)).union(static_series_time_2)
    else:
        temp = set(set(static_series_time_1) & set(a)).union(static_series_time_1)
    return list(temp)

def check_empty_and_fill(a,b,c,d,e):
    sections = []
    days = ['monday','tuesday','wednesday','thursday','friday']
    for i in a:
        sections.append(i)
    for i in sections:
        if d not in e[i]:
            continue
        for j in days:
            for k in b:
                if a[i][j][k] == '':
                    check = check_if_required_slot_empty(a,i,j,k,c,sections,d)
                    if check:
                        a = fill_empty_slot_with_subject(a,i,j,k,c,d)
                        break
                else:
                    check = False
            if check:
                break
        if check:
            check = False
            continue
    return a

def check_if_required_slot_empty(a,b,c,d,e,other_sections,course):
    check = True
    for i in range(e):
        if a[b][c][static_series_time_1[static_series_time_1.index(d)+i]] == '':
            check = True
        else:
            check = False
            return check
    if check:
        check = check_slot_empty_in_other_sections(a,b,c,d,e,other_sections,course)
    return check

def check_slot_empty_in_other_sections(a,b,c,d,e,other_sections,course):
    check = True
    for i in other_sections:
        if i != b:
            for j in range(e):
                if a[i][c][static_series_time_1[static_series_time_1.index(d)+j]] != course or a[i][c][static_series_time_1[static_series_time_1.index(d)+j]] == '':
                    check = True
                else:
                    check = False
                    return check
    return check

def fill_empty_slot_with_subject(a,b,c,d,e,f):
    for i in range(e):
        a[b][c][static_series_time_1[static_series_time_1.index(d)+i]] = f
    return a