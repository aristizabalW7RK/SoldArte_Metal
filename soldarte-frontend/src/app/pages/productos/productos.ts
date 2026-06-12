import { Component, inject, signal } from '@angular/core';
import { ProductoService, Producto } from '../../services/productos';

@Component({
  selector: 'app-productos',
  imports: [],
  templateUrl: './productos.html',
  styleUrl: './productos.css',
})
export class Productos {
  private productoService = inject(ProductoService);

  productos = signal<Producto[]>([]);
  cargando = signal(true);
  soloDisponibles = signal(true);

  constructor() {
    this.cargarProductos();
  }

  cargarProductos() {
    this.cargando.set(true);
    this.productoService.obtenerProductos(this.soloDisponibles()).subscribe({
      next: prods => {
        this.productos.set(prods);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false),
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
