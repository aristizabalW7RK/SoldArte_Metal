import { Component, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { TemaService } from '../../services/tema';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  menuAbierto = signal(false);

  constructor(public temaService: TemaService) {}

  toggleMenu() {
    this.menuAbierto.set(!this.menuAbierto());
  }
}