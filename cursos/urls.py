from django.urls import path
from . import views

urlpatterns = [

    # 1. Listar cursos (CBV)
    path('web/cursos/', views.CursoListView.as_view(), name='web_lista_cursos'),

    # 2. Crear curso (CBV)
    path('web/cursos/nuevo/', views.CursoCreateView.as_view(), name='web_crear_curso'),

    # 3. Editar curso (CBV)
    path('web/cursos/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='web_editar_curso'),

    # 4. Eliminar curso (CBV)
    path('web/cursos/<int:pk>/eliminar/', views.CursoDeleteView.as_view(), name='web_eliminar_curso'),

    # 5. Detalle de curso (CBV)
    path('web/cursos/<int:pk>/', views.CursoDetailView.as_view(), name='web_detalle_curso'),

    # 6. Detalle de profesor (Refactorizado a CBV para el Reto)
    path('web/profesor/<int:pk>/', views.ProfesorDetailView.as_view(), name='web_detalle_profesor'),

    # 7. Catálogo de profesores con paginación
    path('web/profesores/', views.ProfesorListView.as_view(), name='web_lista_profesores'),

    # 8. Listar estudiantes (Paginada)
    path('web/estudiantes/', views.EstudianteListView.as_view(), name='web_lista_estudiantes'),
    
    # 9. Detalle de estudiante
    path('web/estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(), name='web_detalle_estudiante'),
    
    # 10. Crear estudiante (Protegido)
    path('web/estudiantes/nuevo/', views.EstudianteCreateView.as_view(), name='web_crear_estudiante'),
    
    # 11. Editar estudiante
    path('web/estudiantes/<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='web_editar_estudiante'),
    
    # 12. Eliminar estudiante
    path('web/estudiantes/<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='web_eliminar_estudiante'),

    # 13. Inscribir estudiante a un curso (Reto 2)
    path('web/estudiantes/<int:pk>/inscribir/', views.InscribirEstudianteView.as_view(), name='web_inscribir_estudiante'),
]
