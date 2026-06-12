import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  imports: [RouterLink, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = signal('');
  password = signal('');
  error = signal('');
  cargando = signal(false);

  iniciarSesion() {
    if (!this.email() || !this.password()) {
      this.error.set('Todos los campos son obligatorios');
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    this.authService.login({ email: this.email(), password: this.password() }).subscribe({
      next: () => this.router.navigate(['/']),
      error: err => {
        this.error.set(err.error?.detail || 'Error al iniciar sesión');
        this.cargando.set(false);
      },
    });
  }
}
