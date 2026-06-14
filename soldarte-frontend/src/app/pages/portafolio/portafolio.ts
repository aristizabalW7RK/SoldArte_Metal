import { Component, inject, signal, computed } from '@angular/core';
import { PortafolioService, Categoria, Obra } from '../../services/portafolio';
import { SkeletonComponent } from '../../components/skeleton/skeleton';

@Component({
  selector: 'app-portafolio',
  imports: [SkeletonComponent],
  templateUrl: './portafolio.html',
  styleUrl: './portafolio.css',
})
export class Portafolio {
  private portafolioService = inject(PortafolioService);

  categorias = signal<Categoria[]>([]);
  obras = signal<Obra[]>([]);
  categoriaSeleccionada = signal<number | null>(null);
  cargando = signal(true);
  error = signal('');
  imagenSeleccionada = signal<string | null>(null);
  indiceImagen = signal(0);
  obraActual = signal<Obra | null>(null);

  obrasFiltradas = computed(() => {
    const catId = this.categoriaSeleccionada();
    if (!catId) return this.obras();
    return this.obras().filter(o => o.categoria_id === catId);
  });

  constructor() {
    this.cargarDatos();
  }

  private cargarDatos() {
    this.cargando.set(true);
    this.error.set('');
    this.portafolioService.obtenerCategorias().subscribe({
      next: cats => this.categorias.set(cats),
      error: () => {},
    });
    this.portafolioService.obtenerObras().subscribe({
      next: obras => {
        this.obras.set(obras);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('Error al cargar el portafolio. Intenta de nuevo más tarde.');
        this.cargando.set(false);
      },
    });
  }

  reintentar() {
    this.cargarDatos();
  }

  filtrarPorCategoria(id: number | null) {
    this.categoriaSeleccionada.set(id);
  }

  abrirLightbox(obra: Obra, indice: number) {
    this.obraActual.set(obra);
    this.indiceImagen.set(indice);
    this.imagenSeleccionada.set(obra.imagenes[indice].url);
  }

  anteriorImagen() {
    const obra = this.obraActual();
    if (!obra) return;
    const nuevo = this.indiceImagen() - 1;
    if (nuevo >= 0) {
      this.indiceImagen.set(nuevo);
      this.imagenSeleccionada.set(obra.imagenes[nuevo].url);
    }
  }

  siguienteImagen() {
    const obra = this.obraActual();
    if (!obra) return;
    const nuevo = this.indiceImagen() + 1;
    if (nuevo < obra.imagenes.length) {
      this.indiceImagen.set(nuevo);
      this.imagenSeleccionada.set(obra.imagenes[nuevo].url);
    }
  }

  cerrarLightbox() {
    this.imagenSeleccionada.set(null);
    this.obraActual.set(null);
  }
}
