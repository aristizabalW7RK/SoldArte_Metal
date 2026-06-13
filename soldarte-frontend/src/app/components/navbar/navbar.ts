import { Component, signal, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { TemaService } from '../../services/tema';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  menuAbierto = signal(false);
  usuarioDesplegado = signal(false);
  authService = inject(AuthService);
  private router = inject(Router);

  constructor(public temaService: TemaService) {}

  toggleMenu() {
    this.menuAbierto.set(!this.menuAbierto());
  }

  toggleUsuario() {
    this.usuarioDesplegado.set(!this.usuarioDesplegado());
  }

  logout() {
    this.authService.logout();
    this.usuarioDesplegado.set(false);
    this.router.navigate(['/']);
  }
}
