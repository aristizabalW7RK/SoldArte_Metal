import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs';
import { ApiService } from './api';

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string | null;
}

export interface ImagenObra {
  id: number;
  url: string;
  es_portada: boolean;
  orden: number;
}

export interface Obra {
  id: number;
  categoria_id: number;
  titulo: string;
  descripcion: string | null;
  ubicacion: string | null;
  fecha_realizacion: string | null;
  destacado: boolean;
  created_at: string;
  categoria: Categoria;
  imagenes: ImagenObra[];
}

@Injectable({ providedIn: 'root' })
export class PortafolioService {
  private api = inject(ApiService);

  obtenerCategorias() {
    return this.api.get<Categoria[]>('/api/portafolio/categorias');
  }

  obtenerObras(categoriaId?: number) {
    const params: Record<string, string> = {};
    if (categoriaId) params['categoria_id'] = String(categoriaId);
    return this.api.get<Obra[]>('/api/portafolio/obras', params)
      .pipe(
        map(obras => obras.map(obra => ({
          ...obra,
          imagenes: obra.imagenes.map(img => ({
            ...img,
            url: `${this.api.baseUrl}${img.url}`
          }))
        })))
      );
  }
}
