import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

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
  telefono = signal('');
  fechaNacimiento = signal('');
  password = signal('');
  error = signal('');
  cargando = signal(false);
  exitoso = signal(false);

  crearCuenta() {
    if (!this.nombre() || !this.email() || !this.password()) {
      this.error.set('Nombre, email y contraseña son obligatorios');
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    const datos = {
      nombre: this.nombre(),
      email: this.email(),
      password: this.password(),
      telefono: this.telefono() || undefined,
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
