from app.models import RelCourse, Courses, StuClasstable, Classes, ClassTime, Students, RelStuCtable
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=1000)
def write_result():
    # try:
    #     c = Classes.objects.all()
    #     for ele in c:
    #         cap = ele.capacity
    #         ta = StuClasstable.objects.filter(classobj_id=ele.id).order_by('-coin')
    #         re_num = ta.count()
    #         count = 0
    #         for re in ta:
    #             if count < cap:
    #                 re.status = RelStuCtable.objects.get(status='selected')
    #             else:
    #                 re.status = RelStuCtable.objects.get(status='unselected')
    #             re.save()
    #             count += 1
    #
    #     return True
    # except Exception as e:
    #     print(e)
    #     return False
    print("Scheduler started!")

register_events(scheduler)

scheduler.start()