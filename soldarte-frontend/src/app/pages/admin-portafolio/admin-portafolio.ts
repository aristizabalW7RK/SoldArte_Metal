import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { PortafolioService, Categoria, Obra } from '../../services/portafolio';

@Component({
  selector: 'app-admin-portafolio',
  imports: [FormsModule, RouterLink],
  templateUrl: './admin-portafolio.html',
  styleUrl: './admin-portafolio.css',
})
export class AdminPortafolio {
  private api = inject(ApiService);
  private portafolioService = inject(PortafolioService);

  categorias = signal<Categoria[]>([]);
  obras = signal<Obra[]>([]);
  cargando = signal(false);

  // Categoria form
  catNombre = signal('');
  catDescripcion = signal('');
  catError = signal('');
  catExitoso = signal(false);

  // Obra form
  obrTitulo = signal('');
  obrDescripcion = signal('');
  obrCategoriaId = signal<number | null>(null);
  obrUbicacion = signal('');
  obrFecha = signal('');
  obrDestacado = signal(false);
  obrError = signal('');
  obrExitoso = signal(false);

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
    this.portafolioService.obtenerCategorias().subscribe({
      next: cats => this.categorias.set(cats),
      error: err => this.catError.set(err.error?.detail || 'Error al cargar categorías'),
    });
    this.portafolioService.obtenerObras().subscribe({
      next: obs => this.obras.set(obs),
      error: err => this.obrError.set(err.error?.detail || 'Error al cargar obras'),
    });
  }

  crearCategoria() {
    if (!this.catNombre()) {
      this.catError.set('El nombre es obligatorio');
      return;
    }
    this.cargando.set(true);
    this.catError.set('');
    this.catExitoso.set(false);
    this.api.post<Categoria>('/api/portafolio/categorias', {
      nombre: this.catNombre(),
      descripcion: this.catDescripcion() || null,
    }).subscribe({
      next: () => {
        this.catExitoso.set(true);
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

  crearObra() {
    if (!this.obrTitulo() || !this.obrCategoriaId()) {
      this.obrError.set('Título y categoría son obligatorios');
      return;
    }
    this.cargando.set(true);
    this.obrError.set('');
    this.obrExitoso.set(false);
    this.api.post<Obra>('/api/portafolio/obras', {
      categoria_id: this.obrCategoriaId(),
      titulo: this.obrTitulo(),
      descripcion: this.obrDescripcion() || null,
      ubicacion: this.obrUbicacion() || null,
      fecha_realizacion: this.obrFecha() || null,
      destacado: this.obrDestacado(),
    }).subscribe({
      next: obra => {
        this.obrExitoso.set(true);
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
        this.obraIdImagen.set(null);
        this.imagenCargando.set(false);
        this.cargarDatos();
      },
      error: err => {
        this.imagenError.set(err.error?.detail || 'Error al subir imagen');
        this.imagenCargando.set(false);
      },
    });
  }
}
