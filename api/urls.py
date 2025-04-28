from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]