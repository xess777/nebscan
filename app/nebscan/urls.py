from rest_framework import routers

from .serializers import NebBlockViewSet


router = routers.DefaultRouter()
router.register(r'blocks', NebBlockViewSet)

urlpatterns = router.urls
