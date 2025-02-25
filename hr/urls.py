from rest_framework import routers

from hr.views import GetResume

router = routers.DefaultRouter()
router.register(r'get_resume', GetResume, basename='resume')
urlpatterns = router.urls

# urlpatterns += router.urls