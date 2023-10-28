from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Hunting Blog API",
        default_version='v1',
        description="Personal blog about hunting and outdoor activities with a system of user comments and likes.",
        terms_of_service="https://github.com/yurii-onyshchuk/HuntingBlog#license",
        contact=openapi.Contact(email="yura.onyshchuk@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
