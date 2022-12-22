from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from apps.story.views import frontpage, search, submit, newest, vote, story, listing, viewDocumentInvoice,printAllVersions
from apps.core.views import signup

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('s/<int:story_id>/vote/', vote, name='vote'),
    path('s/<int:story_id>/', story, name='story'),
    path('versions/<int:project_id>/', listing, name='versions'),

    path('versionspdf/<int:versionID>/', viewDocumentInvoice, name='version_pdf'),

    path('allversionspdf/<int:projectID>/', printAllVersions, name='all_version_pdf'),
    # path('test-sql/', test_sql, name='test-sql'),

    
    path('u/', include('apps.userprofile.urls')),
    path('newest/', newest, name='newest'),
    path('search/', search, name='search'),
    path('submit/', submit, name='submit'),
    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]
