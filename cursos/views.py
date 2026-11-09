from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Curso, Profesor, Estudiante  # Importamos todos los modelos
from .forms import CursoForm, EstudianteForm    # Importamos ambos formularios
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.db.models import Q  # <--- AGREGADO: Necesario para usar filtros avanzados (OR)

# 1. VISTAS PÚBLICAS (Accesibles sin iniciar sesión)
class CursoListView(ListView):
    model = Curso
    template_name = 'cursos/lista.html'
    context_object_name = 'cursos'
    paginate_by = 6  # Muestra máximo 6 cursos por página

    # <--- INTEGRADO: Método para procesar la barra de búsqueda
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q') # Captura el parámetro ?q= de la URL
        if query:
            # Filtra en el nombre del curso OR en el código OR en el nombre del profesor
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(codigo__icontains=query) | 
                Q(profesor__nombre__icontains=query)
            )
        return queryset

    # <--- INTEGRADO: Método para mantener el texto buscado dentro del input HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'cursos/detalle.html'
    context_object_name = 'curso'


# 2. VISTAS PROTEGIDAS (Requieren usuario autenticado)
class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue creado exitosamente!"  # Mensaje flash de éxito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Curso (Protegido)'
        return context


class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue actualizado correctamente!"  # Mensaje flash de éxito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Curso: {self.object.nombre}'
        return context

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    success_url = reverse_lazy('web_lista_cursos')
    context_object_name = 'curso'

    # Mensaje flash de advertencia al confirmar la eliminación
    def form_valid(self, form):
        messages.warning(self.request, f"El curso '{self.object.nombre}' fue eliminado del sistema.")
        return super().form_valid(form)


# 3. DETALLE DEL PROFESOR
class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'cursos/profesor_detalle.html'
    context_object_name = 'profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = self.object.cursos.all() 
        return context

# 4. CATÁLOGO DE PROFESORES CON PAGINACIÓN
class ProfesorListView(ListView):
    model = Profesor
    template_name = 'cursos/profesores_lista.html'
    context_object_name = 'profesores'
    paginate_by = 3  # Muestra máximo 3 profesores por página


# 1. LISTA DE ESTUDIANTES (Paginada con Buscador Corregido)
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'cursos/estudiantes_lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 5

    def get_queryset(self):
        """
        Filtra los estudiantes únicamente por los campos existentes: nombre o matricula.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Captura el parámetro ?q= de la URL
        
        if query:
                queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(matricula__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Envía el término buscado a la plantilla de estudiantes.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context



# 2. DETALLE DE ESTUDIANTE
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'cursos/estudiante_detalle.html'
    context_object_name = 'estudiante'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos_disponibles'] = Curso.objects.exclude(estudiantes=self.object)
        context['cursos_inscritos'] = Curso.objects.filter(estudiantes=self.object)
        return context

# 3. CREAR ESTUDIANTE (Protegido + Mensaje Flash)
class EstudianteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡El estudiante '%(nombre)s' fue registrado con éxito!"

# 4. EDITAR ESTUDIANTE
class EstudianteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡Los datos del estudiante '%(nombre)s' fueron actualizados correctamente!"

# 5. ELIMINAR ESTUDIANTE
class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'cursos/estudiante_confirm_delete.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    context_object_name = 'estudiante'

    def form_valid(self, form):
        messages.warning(self.request, f"El estudiante '{self.object.nombre}' fue eliminado.")
        return super().form_valid(form)   
        
# 6. INSCRIBIR ESTUDIANTE A UN CURSO (Reto 2: relación N:M)
class InscribirEstudianteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        estudiante = get_object_or_404(Estudiante, pk=pk)
        curso = get_object_or_404(Curso, pk=request.POST.get('curso_id'))

        curso.estudiantes.add(estudiante)   # ORM: crea el vínculo N:M

        messages.success(request, f"'{estudiante.nombre}' fue inscrito en el curso '{curso.nombre}'.")
        return redirect('web_detalle_estudiante', pk=estudiante.pk)
