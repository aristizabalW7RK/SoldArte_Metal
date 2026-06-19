import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';
import { ApiService } from './api';

export interface ImagenProducto {
  id: number;
  url: string;
  es_portada: boolean;
  orden: number;
}

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string | null;
  referencia: string | null;
  precio: string;
  stock: number;
  disponible: boolean;
  imagen_url: string | null;
  imagenes: ImagenProducto[];
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class ProductoService {
  private api = inject(ApiService);

  private mapearUrl(base: string) {
    return (p: Producto): Producto => ({
      ...p,
      imagen_url: p.imagen_url ? `${base}${p.imagen_url}` : null,
      imagenes: p.imagenes.map(img => ({
        ...img,
        url: `${base}${img.url}`,
      })),
    });
  }

  obtenerProductos(soloDisponibles = true) {
    const params = { solo_disponibles: String(soloDisponibles) };
    return this.api.get<Producto[]>('/api/productos', params).pipe(
      map(productos => productos.map(this.mapearUrl(this.api.baseUrl))),
    );
  }

  eliminarProducto(id: number) {
    return this.api.delete(`/api/productos/${id}`);
  }
}
