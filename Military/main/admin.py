from django.contrib import admin
from .models import soldier
from .models import task
from .models import specialization
from .models import rank
from .models import TaskAssignment
from .models import difficultylevel
from .models import transport
from .models import educationlevel
from .models import weatherconditions
from .models import tasktype
from .models import location


# Register your models here.

admin.site.register(soldier)
admin.site.register(task)
admin.site.register(specialization)
admin.site.register(rank)
admin.site.register(TaskAssignment)
admin.site.register(difficultylevel)
admin.site.register(transport)
admin.site.register(educationlevel)
admin.site.register(weatherconditions)
admin.site.register(tasktype)
admin.site.register(location)




