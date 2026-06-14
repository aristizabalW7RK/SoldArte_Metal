import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { ApiService } from '../../services/api';
import { SkeletonComponent } from '../../components/skeleton/skeleton';

interface CotizacionAdmin {
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

@Component({
  selector: 'app-admin-cotizaciones',
  imports: [RouterLink, DatePipe, SkeletonComponent],
  templateUrl: './admin-cotizaciones.html',
  styleUrl: './admin-cotizaciones.css',
})
export class AdminCotizaciones {
  private api = inject(ApiService);

  cotizaciones = signal<CotizacionAdmin[]>([]);
  cargando = signal(false);
  error = signal('');

  constructor() {
    this.cargarCotizaciones();
  }

  cargarCotizaciones() {
    this.cargando.set(true);
    this.api.get<CotizacionAdmin[]>('/api/cotizaciones').subscribe({
      next: data => {
        this.cotizaciones.set(data);
        this.cargando.set(false);
      },
      error: err => {
        this.error.set(err.error?.detail || 'Error al cargar cotizaciones');
        this.cargando.set(false);
      },
    });
  }

  cambiarEstado(id: number, estado: string) {
    this.api.patch(`/api/cotizaciones/${id}/estado?estado=${estado}`, {}).subscribe({
      next: () => this.cargarCotizaciones(),
      error: err => this.error.set(err.error?.detail || 'Error al cambiar estado'),
    });
  }
}
