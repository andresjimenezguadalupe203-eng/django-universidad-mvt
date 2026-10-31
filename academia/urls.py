from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import messages  # Importación obligatoria para construir la alerta informativa
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Extendemos la vista nativa de Login para inyectar la alerta informativa (Reto 2)
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        # Al autenticarse correctamente, generamos un mensaje de tipo INFO con el nombre del usuario
        messages.info(self.request, f"¡Bienvenido de nuevo al sistema, {form.get_user().username}!")
        return super().form_valid(form)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints de Autenticación JWT (De tu práctica anterior)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('cursos.api_urls')),
    
    # CONEXIÓN DE LA NUEVA GUÍA: Carga las páginas web HTML
    path('', include('cursos.urls')),
    
    # Rutas Nativas de Autenticación de Django (Modificado para aplicar el Reto 2)
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
