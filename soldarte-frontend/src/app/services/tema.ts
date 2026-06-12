import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TemaService {
  private readonly STORAGE_KEY = 'soldarte-tema';
  oscuro = signal(true);

  constructor() {
    const guardado = localStorage.getItem(this.STORAGE_KEY);
    this.oscuro.set(guardado !== 'claro');
    this.aplicarTema();
  }

  toggleTema() {
    this.oscuro.update(v => !v);
    localStorage.setItem(this.STORAGE_KEY, this.oscuro() ? 'oscuro' : 'claro');
    this.aplicarTema();
  }

  private aplicarTema() {
    document.body.className = this.oscuro() ? 'oscuro' : 'claro';
  }
}