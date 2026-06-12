import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TemaService } from '../../services/tema';
import { CotizacionService } from '../../services/cotizacion';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-cotizacion',
  imports: [FormsModule],
  templateUrl: './cotizacion.html',
  styleUrl: './cotizacion.css',
})
export class Cotizacion {
  private cotizacionService = inject(CotizacionService);
  private authService = inject(AuthService);
  temaService = inject(TemaService);

  nombreCliente = signal('');
  telefono = signal('');
  email = signal('');
  direccion = signal('');
  tipoTrabajo = signal('');
  descripcion = signal('');
  error = signal('');
  cargando = signal(false);
  exitoso = signal(false);

  enviarCotizacion() {
    if (!this.nombreCliente() || !this.telefono() || !this.email() || !this.tipoTrabajo() || !this.descripcion()) {
      this.error.set('Todos los campos obligatorios deben estar diligenciados');
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    const datos = {
      nombre_cliente: this.nombreCliente(),
      telefono: this.telefono(),
      email: this.email(),
      tipo_trabajo: this.tipoTrabajo(),
      descripcion: this.descripcion(),
      direccion: this.direccion() || undefined,
      usuario_id: this.authService.usuarioId ?? undefined,
    };
    this.cotizacionService.crear(datos).subscribe({
      next: () => {
        this.exitoso.set(true);
        this.cargando.set(false);
        this.nombreCliente.set('');
        this.telefono.set('');
        this.email.set('');
        this.direccion.set('');
        this.tipoTrabajo.set('');
        this.descripcion.set('');
      },
      error: err => {
        this.error.set(err.error?.detail || 'Error al enviar la cotización');
        this.cargando.set(false);
      },
    });
  }
}
