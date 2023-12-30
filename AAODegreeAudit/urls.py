"""
URL configuration for AAODegreeAudit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from DegreeAudit import views

urlpatterns = ([
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('audit/<int:_id>', views.audit, name="audit"),
    path('save_form/<int:_id>', views.save_form, name="save_form"),
    path('student_list/', views.student_list, name="student_list"),
    path('student_list/student/<int:_id>', views.student_show, name="student_show")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
