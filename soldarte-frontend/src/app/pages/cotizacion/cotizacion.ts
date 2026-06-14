import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TemaService } from '../../services/tema';
import { CotizacionService } from '../../services/cotizacion';
import { AuthService } from '../../services/auth';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function formatearTelefono(digitos: string): string {
  const d = digitos.replace(/\D/g, '').slice(0, 10);
  if (d.length <= 3) return d;
  if (d.length <= 6) return `${d.slice(0, 3)} ${d.slice(3)}`;
  return `${d.slice(0, 3)} ${d.slice(3, 6)} ${d.slice(6)}`;
}

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
  telefonoDigitos = signal('');
  telefonoFormateado = computed(() => formatearTelefono(this.telefonoDigitos()));
  telefonoCompleto = computed(() => this.telefonoDigitos().length === 10 && this.telefonoDigitos().startsWith('3'));
  email = signal('');
  emailValido = computed(() => !this.email() || EMAIL_RE.test(this.email()));
  direccion = signal('');
  tipoTrabajo = signal('');
  descripcion = signal('');
  error = signal('');
  cargando = signal(false);
  exitoso = signal(false);

  onTelefonoInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const soloDigitos = input.value.replace(/\D/g, '').slice(0, 10);
    this.telefonoDigitos.set(soloDigitos);
    input.value = formatearTelefono(soloDigitos);
  }

  enviarCotizacion() {
    if (!this.nombreCliente()) { this.error.set('El nombre es obligatorio'); return; }
    if (!this.telefonoCompleto()) { this.error.set('El teléfono debe ser un celular colombiano de 10 dígitos (ej: 304 143 1918)'); return; }
    if (!this.email() || !this.emailValido()) { this.error.set('El correo electrónico no es válido'); return; }
    if (!this.tipoTrabajo()) { this.error.set('Selecciona un tipo de trabajo'); return; }
    if (!this.descripcion()) { this.error.set('La descripción es obligatoria'); return; }
    this.cargando.set(true);
    this.error.set('');
    const datos = {
      nombre_cliente: this.nombreCliente(),
      telefono: this.telefonoDigitos(),
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
        this.telefonoDigitos.set('');
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
