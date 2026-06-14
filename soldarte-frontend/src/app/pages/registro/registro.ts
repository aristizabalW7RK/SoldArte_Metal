import { Component, computed, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function formatearTelefono(digitos: string): string {
  const d = digitos.replace(/\D/g, '').slice(0, 10);
  if (d.length <= 3) return d;
  if (d.length <= 6) return `${d.slice(0, 3)} ${d.slice(3)}`;
  return `${d.slice(0, 3)} ${d.slice(3, 6)} ${d.slice(6)}`;
}

@Component({
  selector: 'app-registro',
  imports: [RouterLink, FormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.css',
})
export class Registro {
  private authService = inject(AuthService);
  private router = inject(Router);

  nombre = signal('');
  email = signal('');
  telefonoDigitos = signal('');
  telefonoFormateado = computed(() => formatearTelefono(this.telefonoDigitos()));
  telefonoCompleto = computed(() => this.telefonoDigitos().length === 10 && this.telefonoDigitos().startsWith('3'));
  fechaNacimiento = signal('');
  password = signal('');
  error = signal('');
  cargando = signal(false);
  exitoso = signal(false);

  pwLargo = computed(() => this.password().length >= 8);
  pwMayuscula = computed(() => /[A-Z]/.test(this.password()));
  pwMinuscula = computed(() => /[a-z]/.test(this.password()));
  pwNumero = computed(() => /\d/.test(this.password()));
  pwSimbolo = computed(() => /[!@#$%^&*()_\-+=\[\]{}|;:'",.<>?/\\~`]/.test(this.password()));

  emailValido = computed(() => !this.email() || EMAIL_RE.test(this.email()));

  onTelefonoInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const soloDigitos = input.value.replace(/\D/g, '').slice(0, 10);
    this.telefonoDigitos.set(soloDigitos);
    input.value = formatearTelefono(soloDigitos);
  }

  private erroresValidacion(): string[] {
    const errores: string[] = [];
    if (!this.nombre()) errores.push('El nombre es obligatorio');
    if (!this.email()) errores.push('El correo electrónico es obligatorio');
    else if (!this.emailValido()) errores.push('El correo electrónico no es válido');
    if (this.telefonoDigitos() && !this.telefonoCompleto()) errores.push('El teléfono debe ser un celular colombiano de 10 dígitos (ej: 304 143 1918)');
    if (!this.password()) errores.push('La contraseña es obligatoria');
    else {
      if (!this.pwLargo()) errores.push('Mínimo 8 caracteres');
      if (!this.pwMayuscula()) errores.push('Falta una mayúscula');
      if (!this.pwMinuscula()) errores.push('Falta una minúscula');
      if (!this.pwNumero()) errores.push('Falta un número');
      if (!this.pwSimbolo()) errores.push('Falta un símbolo especial');
    }
    return errores;
  }

  crearCuenta() {
    const errores = this.erroresValidacion();
    if (errores.length) {
      this.error.set(errores.join('. '));
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    const datos = {
      nombre: this.nombre(),
      email: this.email(),
      password: this.password(),
      telefono: this.telefonoDigitos() || undefined,
      fecha_nacimiento: this.fechaNacimiento() || undefined,
    };
    this.authService.registro(datos).subscribe({
      next: () => {
        this.exitoso.set(true);
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: err => {
        this.error.set(err.error?.detail || 'Error al crear la cuenta');
        this.cargando.set(false);
      },
    });
  }
}
