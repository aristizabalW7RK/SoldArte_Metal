import { Injectable, inject, signal } from '@angular/core';
import { tap } from 'rxjs';
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

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UsuarioResponse {
  id: number;
  nombre: string;
  email: string;
  telefono: string | null;
  es_admin: boolean;
  created_at: string;
}

interface JwtPayload {
  sub: string;
  nombre: string;
  email: string;
  es_admin: boolean;
  exp: number;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = inject(ApiService);
  private readonly TOKEN_KEY = 'soldarte-token';

  usuario = signal<{
    id: number;
    nombre: string;
    email: string;
    es_admin: boolean;
  } | null>(null);

  constructor() {
    this.cargarUsuarioDesdeToken();
  }

  private cargarUsuarioDesdeToken() {
    const payload = this.obtenerPayload();
    if (payload) {
      this.usuario.set({
        id: Number(payload['sub']),
        nombre: (payload['nombre'] as string) ?? 'Usuario',
        email: (payload['email'] as string) ?? '',
        es_admin: (payload['es_admin'] as boolean) ?? false,
      });
    }
  }

  private obtenerPayload(): Record<string, unknown> | null {
    const t = this.token;
    if (!t) return null;
    try {
      return JSON.parse(atob(t.split('.')[1]));
    } catch {
      return null;
    }
  }

  get token(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
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
    return !!this.token;
  }

  registro(datos: RegistroData) {
    return this.api.post<UsuarioResponse>('/api/auth/registro', datos);
  }

  login(datos: LoginData) {
    return this.api.post<TokenResponse>('/api/auth/login', datos).pipe(
      tap(res => {
        localStorage.setItem(this.TOKEN_KEY, res.access_token);
        this.cargarUsuarioDesdeToken();
      }),
    );
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    this.usuario.set(null);
  }
}
