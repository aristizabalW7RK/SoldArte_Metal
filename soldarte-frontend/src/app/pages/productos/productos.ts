import { Component, inject, signal } from '@angular/core';
import { ProductoService, Producto } from '../../services/productos';
import { SkeletonComponent } from '../../components/skeleton/skeleton';

@Component({
  selector: 'app-productos',
  imports: [SkeletonComponent],
  templateUrl: './productos.html',
  styleUrl: './productos.css',
})
export class Productos {
  private productoService = inject(ProductoService);

  productos = signal<Producto[]>([]);
  cargando = signal(true);
  error = signal('');
  soloDisponibles = signal(true);

  constructor() {
    this.cargarProductos();
  }

  cargarProductos() {
    this.cargando.set(true);
    this.error.set('');
    this.productoService.obtenerProductos(this.soloDisponibles()).subscribe({
      next: prods => {
        this.productos.set(prods);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('Error al cargar productos. Intenta de nuevo más tarde.');
        this.cargando.set(false);
      },
    });
  }

  toggleDisponibles() {
    this.soloDisponibles.update(v => !v);
    this.cargarProductos();
  }

  formatearPrecio(precio: string): string {
    const num = Number(precio);
    return '$' + num.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }
}
