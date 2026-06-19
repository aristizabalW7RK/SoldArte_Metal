import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { PortafolioService, Categoria, Obra } from '../../services/portafolio';
import { SkeletonComponent } from '../../components/skeleton/skeleton';

@Component({
  selector: 'app-admin-portafolio',
  imports: [FormsModule, RouterLink, SkeletonComponent],
  templateUrl: './admin-portafolio.html',
  styleUrl: './admin-portafolio.css',
})
export class AdminPortafolio {
  private api = inject(ApiService);
  private portafolioService = inject(PortafolioService);

  categorias = signal<Categoria[]>([]);
  obras = signal<Obra[]>([]);
  cargando = signal(false);
  cargandoLista = signal(true);

  // Categoria form
  catNombre = signal('');
  catDescripcion = signal('');
  catError = signal('');
  catExitoso = signal('');
  catEditando = signal<Categoria | null>(null);

  // Obra form
  obrTitulo = signal('');
  obrDescripcion = signal('');
  obrCategoriaId = signal<number | null>(null);
  obrUbicacion = signal('');
  obrFecha = signal('');
  obrDestacado = signal(false);
  obrError = signal('');
  obrExitoso = signal('');
  obraEditando = signal<Obra | null>(null);

  // Image upload
  imagenFile: File | null = null;
  imagenPortada = signal(false);
  obraIdImagen = signal<number | null>(null);
  imagenError = signal('');
  imagenCargando = signal(false);

  // Lightbox
  imagenSeleccionada = signal<string | null>(null);

  constructor() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargandoLista.set(true);
    this.portafolioService.obtenerCategorias().subscribe({
      next: cats => this.categorias.set(cats),
      error: err => this.catError.set(err.error?.detail || 'Error al cargar categorías'),
    });
    this.portafolioService.obtenerObras().subscribe({
      next: obs => {
        this.obras.set(obs);
        this.cargandoLista.set(false);
      },
      error: err => {
        this.obrError.set(err.error?.detail || 'Error al cargar obras');
        this.cargandoLista.set(false);
      },
    });
  }

  // --- Categorías ---

  crearCategoria() {
    if (!this.catNombre()) {
      this.catError.set('El nombre es obligatorio');
      return;
    }
    this.cargando.set(true);
    this.catError.set('');
    this.catExitoso.set('');

    if (this.catEditando()) {
      const id = this.catEditando()!.id;
      this.api.put<Categoria>(`/api/portafolio/categorias/${id}`, {
        nombre: this.catNombre(),
        descripcion: this.catDescripcion() || null,
      }).subscribe({
        next: () => {
          this.catExitoso.set('Categoría actualizada');
          this.cancelarEdicionCategoria();
          this.cargando.set(false);
          this.cargarDatos();
        },
        error: err => {
          this.catError.set(err.error?.detail || 'Error al actualizar categoría');
          this.cargando.set(false);
        },
      });
    } else {
      this.api.post<Categoria>('/api/portafolio/categorias', {
        nombre: this.catNombre(),
        descripcion: this.catDescripcion() || null,
      }).subscribe({
        next: () => {
          this.catExitoso.set('Categoría creada');
          this.cargando.set(false);
          this.catNombre.set('');
          this.catDescripcion.set('');
          this.cargarDatos();
        },
        error: err => {
          this.catError.set(err.error?.detail || 'Error al crear categoría');
          this.cargando.set(false);
        },
      });
    }
  }

  editarCategoria(cat: Categoria) {
    this.catEditando.set(cat);
    this.catNombre.set(cat.nombre);
    this.catDescripcion.set(cat.descripcion || '');
    this.catError.set('');
    this.catExitoso.set('');
  }

  cancelarEdicionCategoria() {
    this.catEditando.set(null);
    this.catNombre.set('');
    this.catDescripcion.set('');
  }

  eliminarCategoria(id: number) {
    if (!confirm('¿Eliminar esta categoría? Las obras asociadas se quedarán sin categoría.')) return;
    this.api.delete(`/api/portafolio/categorias/${id}`).subscribe({
      next: () => {
        this.catExitoso.set('Categoría eliminada');
        this.cargarDatos();
      },
      error: err => this.catError.set(err.error?.detail || 'Error al eliminar categoría'),
    });
  }

  // --- Obras ---

  crearObra() {
    if (!this.obrTitulo() || !this.obrCategoriaId()) {
      this.obrError.set('Título y categoría son obligatorios');
      return;
    }
    this.cargando.set(true);
    this.obrError.set('');
    this.obrExitoso.set('');

    if (this.obraEditando()) {
      const id = this.obraEditando()!.id;
      this.api.put<Obra>(`/api/portafolio/obras/${id}`, {
        categoria_id: this.obrCategoriaId(),
        titulo: this.obrTitulo(),
        descripcion: this.obrDescripcion() || null,
        ubicacion: this.obrUbicacion() || null,
        fecha_realizacion: this.obrFecha() || null,
        destacado: this.obrDestacado(),
      }).subscribe({
        next: () => {
          this.obrExitoso.set('Obra actualizada');
          this.cancelarEdicionObra();
          this.cargando.set(false);
          this.cargarDatos();
        },
        error: err => {
          this.obrError.set(err.error?.detail || 'Error al actualizar obra');
          this.cargando.set(false);
        },
      });
    } else {
      this.api.post<Obra>('/api/portafolio/obras', {
        categoria_id: this.obrCategoriaId(),
        titulo: this.obrTitulo(),
        descripcion: this.obrDescripcion() || null,
        ubicacion: this.obrUbicacion() || null,
        fecha_realizacion: this.obrFecha() || null,
        destacado: this.obrDestacado(),
      }).subscribe({
        next: obra => {
          this.obrExitoso.set('Obra creada');
          this.cargando.set(false);
          this.obraIdImagen.set(obra.id);
          this.obrTitulo.set('');
          this.obrDescripcion.set('');
          this.obrUbicacion.set('');
          this.obrFecha.set('');
          this.obrDestacado.set(false);
          this.cargarDatos();
        },
        error: err => {
          this.obrError.set(err.error?.detail || 'Error al crear obra');
          this.cargando.set(false);
        },
      });
    }
  }

  editarObra(obra: Obra) {
    this.obraEditando.set(obra);
    this.obrTitulo.set(obra.titulo);
    this.obrDescripcion.set(obra.descripcion || '');
    this.obrCategoriaId.set(obra.categoria_id);
    this.obrUbicacion.set(obra.ubicacion || '');
    this.obrFecha.set(obra.fecha_realizacion || '');
    this.obrDestacado.set(obra.destacado);
    this.obrError.set('');
    this.obrExitoso.set('');
    this.obraIdImagen.set(obra.id);
  }

  cancelarEdicionObra() {
    this.obraEditando.set(null);
    this.obrTitulo.set('');
    this.obrDescripcion.set('');
    this.obrCategoriaId.set(null);
    this.obrUbicacion.set('');
    this.obrFecha.set('');
    this.obrDestacado.set(false);
    this.obraIdImagen.set(null);
  }

  onImagenSeleccionada(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.imagenFile = input.files[0];
    }
  }

  eliminarObra(id: number) {
    if (!confirm('¿Eliminar esta obra?')) return;
    this.api.delete(`/api/portafolio/obras/${id}`).subscribe({
      next: () => this.cargarDatos(),
      error: err => this.obrError.set(err.error?.detail || 'Error al eliminar obra'),
    });
  }

  subirImagen() {
    if (!this.imagenFile || !this.obraIdImagen()) return;
    this.imagenCargando.set(true);
    this.imagenError.set('');
    const formData = new FormData();
    formData.append('file', this.imagenFile);
    formData.append('es_portada', String(this.imagenPortada()));
    this.api.post(`/api/portafolio/obras/${this.obraIdImagen()}/imagenes`, formData).subscribe({
      next: () => {
        this.imagenFile = null;
        this.imagenPortada.set(false);
        this.imagenCargando.set(false);
        this.cargarDatos();
      },
      error: err => {
        this.imagenError.set(err.error?.detail || 'Error al subir imagen');
        this.imagenCargando.set(false);
      },
    });
  }

  eliminarImagen(obraId: number, imagenId: number) {
    if (!confirm('¿Eliminar esta imagen?')) return;
    this.api.delete(`/api/portafolio/obras/${obraId}/imagenes/${imagenId}`).subscribe({
      next: () => this.cargarDatos(),
      error: err => this.obrError.set(err.error?.detail || 'Error al eliminar imagen'),
    });
  }
}
