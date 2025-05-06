from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from imagetotextapp.views import ExtractionsViewSet
from django.contrib import admin
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
# router.register('create-extraction-model', views.CreateExtractionModelViewSet)
# router.register('upload-files-model', views.UploadFilesModelViewSet)
# router.register('file-upload-model', views.FileUploadViewSet)
router.register('extractions', ExtractionsViewSet)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    # path('images/', ImageListView.as_view(), name='image-list'),
    # path('create-extraction/', CreateExtractionView.as_view(),
    #      name='create-extraction'),
    # path('upload-files/', UploadFilesView.as_view(), name='upload-files'),
    # path('get-batch-results/', AddBatchResult.as_view(),
    #      name='get-batch-results'),
    # path('items/', ItemListView.as_view(), name='item-list'),
    # path('files-upload/', FileUploadView.as_view(), name='files-upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
