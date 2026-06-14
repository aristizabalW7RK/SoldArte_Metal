import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';
import { ApiService } from './api';

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string | null;
  referencia: string | null;
  precio: string;
  stock: number;
  disponible: boolean;
  imagen_url: string | null;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class ProductoService {
  private api = inject(ApiService);

  obtenerProductos(soloDisponibles = true) {
    const params = { solo_disponibles: String(soloDisponibles) };
    return this.api.get<Producto[]>('/api/productos', params).pipe(
      map(productos => productos.map(p => ({
        ...p,
        imagen_url: p.imagen_url ? `${this.api.baseUrl}${p.imagen_url}` : null,
      }))),
    );
  }

  eliminarProducto(id: number) {
    return this.api.delete(`/api/productos/${id}`);
  }
}
