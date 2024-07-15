from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from imagetotextapp import views
from imagetotextapp.views import AddBatchResult, FileUploadView, ImageListView, CreateExtractionView, ItemListView, UploadFilesView


router = routers.DefaultRouter()
router.register('create-extraction-model', views.CreateExtractionModelViewSet)
router.register('upload-files-model', views.UploadFilesModelViewSet)
router.register('file-upload-model', views.FileUploadViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('create-extraction/', CreateExtractionView.as_view(),
         name='create-extraction'),
    path('upload-files/', UploadFilesView.as_view(), name='upload-files'),
    path('get-batch-results/', AddBatchResult.as_view(),
         name='get-batch-results'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('files-upload/', FileUploadView.as_view(), name='files-upload'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
