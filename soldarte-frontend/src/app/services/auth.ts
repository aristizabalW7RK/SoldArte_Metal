import { Injectable, inject, signal } from '@angular/core';
import { finalize, tap } from 'rxjs';
import { ApiService } from './api';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegistroData {
  nombre: string;
  email: string;
  password: string;
  telefono?: string;
  fecha_nacimiento?: string;
}

export interface UsuarioResponse {
  id: number;
  nombre: string;
  email: string;
  telefono: string | null;
  es_admin: boolean;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = inject(ApiService);

  usuario = signal<{
    id: number;
    nombre: string;
    email: string;
    es_admin: boolean;
  } | null>(null);

  /** Resuelve cuando la verificación inicial de /me termina */
  autenticacionLista: Promise<void>;

  private autenticacionResolve!: () => void;

  constructor() {
    this.autenticacionLista = new Promise(resolve => {
      this.autenticacionResolve = resolve;
    });
    this.cargarUsuario();
  }

  private cargarUsuario() {
    this.api.get<UsuarioResponse>('/api/auth/me').subscribe({
      next: res => {
        this.usuario.set(res);
        this.autenticacionResolve();
      },
      error: () => {
        this.usuario.set(null);
        this.autenticacionResolve();
      },
    });
  }

  get usuarioId(): number | null {
    return this.usuario()?.id ?? null;
  }

  get nombre(): string | null {
    return this.usuario()?.nombre ?? null;
  }

  get email(): string | null {
    return this.usuario()?.email ?? null;
  }

  get esAdmin(): boolean {
    return this.usuario()?.es_admin ?? false;
  }

  get estaAutenticado(): boolean {
    return this.usuario() !== null;
  }

  registro(datos: RegistroData) {
    return this.api.post<UsuarioResponse>('/api/auth/registro', datos);
  }

  login(datos: LoginData) {
    return this.api.post<UsuarioResponse>('/api/auth/login', datos).pipe(
      tap(res => this.usuario.set(res)),
    );
  }

  logout() {
    this.api.post('/api/auth/logout', {}).pipe(
      finalize(() => this.usuario.set(null)),
    ).subscribe();
  }
}
