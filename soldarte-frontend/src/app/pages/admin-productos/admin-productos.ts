import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { ProductoService, Producto } from '../../services/productos';
import { SkeletonComponent } from '../../components/skeleton/skeleton';

@Component({
  selector: 'app-admin-productos',
  imports: [FormsModule, RouterLink, SkeletonComponent],
  templateUrl: './admin-productos.html',
  styleUrl: './admin-productos.css',
})
export class AdminProductos {
  private api = inject(ApiService);
  private productoService = inject(ProductoService);

  productos = signal<Producto[]>([]);
  cargando = signal(false);
  cargandoLista = signal(true);

  nombre = signal('');
  descripcion = signal('');
  referencia = signal('');
  precio = signal<number | null>(null);
  stock = signal<number>(0);
  disponible = signal(true);
  error = signal('');
  exitoso = signal('');
  productoEditando = signal<Producto | null>(null);

  imagenFile: File | null = null;
  productoIdImagen: number | null = null;

  constructor() {
    this.cargarProductos();
  }

  cargarProductos() {
    this.cargandoLista.set(true);
    this.productoService.obtenerProductos(false).subscribe({
      next: prods => {
        this.productos.set(prods);
        this.cargandoLista.set(false);
      },
      error: err => {
        this.error.set(err.error?.detail || 'Error al cargar productos');
        this.cargandoLista.set(false);
      },
    });
  }

  crearProducto() {
    if (!this.nombre() || this.precio() === null) {
      this.error.set('Nombre y precio son obligatorios');
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    this.exitoso.set('');

    if (this.productoEditando()) {
      const id = this.productoEditando()!.id;
      this.api.put<Producto>(`/api/productos/${id}`, {
        nombre: this.nombre(),
        descripcion: this.descripcion() || null,
        referencia: this.referencia() || null,
        precio: this.precio(),
        stock: this.stock() || 0,
        disponible: this.disponible(),
      }).subscribe({
        next: () => {
          this.exitoso.set('Producto actualizado');
          this.cancelarEdicionProducto();
          this.cargando.set(false);
          this.cargarProductos();
        },
        error: err => {
          this.error.set(err.error?.detail || 'Error al actualizar producto');
          this.cargando.set(false);
        },
      });
    } else {
      this.api.post<Producto>('/api/productos', {
        nombre: this.nombre(),
        descripcion: this.descripcion() || null,
        referencia: this.referencia() || null,
        precio: this.precio(),
        stock: this.stock() || 0,
        disponible: this.disponible(),
      }).subscribe({
        next: prod => {
          this.exitoso.set('Producto creado correctamente');
          this.cargando.set(false);
          this.nombre.set('');
          this.descripcion.set('');
          this.referencia.set('');
          this.precio.set(null);
          this.stock.set(0);
          this.disponible.set(true);
          this.productoIdImagen = prod.id;
          this.cargarProductos();
        },
        error: err => {
          this.error.set(err.error?.detail || 'Error al crear producto');
          this.cargando.set(false);
        },
      });
    }
  }

  editarProducto(producto: Producto) {
    this.productoEditando.set(producto);
    this.nombre.set(producto.nombre);
    this.descripcion.set(producto.descripcion || '');
    this.referencia.set(producto.referencia || '');
    this.precio.set(Number(producto.precio));
    this.stock.set(producto.stock);
    this.disponible.set(producto.disponible);
    this.error.set('');
    this.exitoso.set('');
  }

  cancelarEdicionProducto() {
    this.productoEditando.set(null);
    this.nombre.set('');
    this.descripcion.set('');
    this.referencia.set('');
    this.precio.set(null);
    this.stock.set(0);
    this.disponible.set(true);
  }

  onImagenSeleccionada(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.imagenFile = input.files[0];
    }
  }

  subirImagen(productoId: number) {
    if (!this.imagenFile) return;
    const formData = new FormData();
    formData.append('file', this.imagenFile);
    this.api.post<Producto>(`/api/productos/${productoId}/imagen`, formData).subscribe({
      next: () => {
        this.imagenFile = null;
        this.productoIdImagen = null;
        this.cargarProductos();
      },
      error: err => this.error.set(err.error?.detail || 'Error al subir imagen'),
    });
  }

  eliminarProducto(id: number) {
    if (!confirm('¿Eliminar este producto?')) return;
    this.productoService.eliminarProducto(id).subscribe({
      next: () => this.cargarProductos(),
      error: err => this.error.set(err.error?.detail || 'Error al eliminar producto'),
    });
  }
}
