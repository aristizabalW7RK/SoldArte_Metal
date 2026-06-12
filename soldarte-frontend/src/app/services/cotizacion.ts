import { Injectable, inject } from '@angular/core';
import { ApiService } from './api';

export interface CotizacionData {
  nombre_cliente: string;
  telefono: string;
  email: string;
  tipo_trabajo: string;
  descripcion: string;
  direccion?: string;
  usuario_id?: number;
}

export interface CotizacionResponse {
  id: number;
  nombre_cliente: string;
  telefono: string;
  email: string;
  tipo_trabajo: string;
  descripcion: string;
  direccion: string | null;
  estado: string;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class CotizacionService {
  private api = inject(ApiService);

  crear(datos: CotizacionData) {
    return this.api.post<CotizacionResponse>('/api/cotizaciones', datos);
  }
}
