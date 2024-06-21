from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from imagetotextapp import views
from imagetotextapp.views import AddBatchResult, ImageUploadView, ImageListView, CreateExtractionView, UploadFilesView, CreateExtractionModelViewSet, UploadFilesModelViewSet


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register('texts', views.TextDataViewSet)
router.register('create-extraction-model', views.CreateExtractionModelViewSet)
router.register('upload-files-model', views.UploadFilesModelViewSet)
# router.register('get-batch-results-model', views.BatchResultModelViewSet)
# router.register('items', views.ItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('create-extraction/', CreateExtractionView.as_view(),
         name='create-extraction'),
    path('upload-files/', UploadFilesView.as_view(), name='upload-files'),
    path('get-batch-results/', AddBatchResult.as_view(),
         name='get-batch-results'),



    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
