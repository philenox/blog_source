from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('photos/', views.PhotosPage.as_view(), name='photos'),
    path('michelle/', views.michelle, name='michelle'),
    path('recipes/', include('recipes.urls')),  # Include recipes URLs
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)