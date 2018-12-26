from django.utils import timezone

from app.models import RelCourse, Courses, StuClasstable, Classes, ClassTime, Students, RelStuCtable, Terms
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")


def write_result():
    try:
        cur= timezone.now()
        end_selected = Terms.objects.get(id=1).end_selected
        if cur>=end_selected:
            c = Classes.objects.all()
            for ele in c:
                cap = ele.capacity
                ta = StuClasstable.objects.filter(classobj_id=ele.id).order_by('-coin')
                re_num = ta.count()
                count = 0
                for re in ta:
                    if count < cap:
                        re.status = RelStuCtable.objects.get(status='selected')
                    re.save()
                    count += 1
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    print("Scheduler started!")
print(timezone.now())
scheduler.add_job(write_result, 'date', run_date='2018-12-27 01:31:30')

register_events(scheduler)

scheduler.start()