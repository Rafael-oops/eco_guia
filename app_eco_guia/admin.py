from django.contrib import admin
from .models import USUARIO, ImageHistory,CATEGORIA, IDEIA, RECLAMACOE
# Register your models here.

admin.site.register(USUARIO)
admin.site.register(ImageHistory)
admin.site.register(CATEGORIA)
admin.site.register(IDEIA)
admin.site.register(RECLAMACOE)
