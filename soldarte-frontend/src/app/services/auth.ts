import { Injectable, inject } from '@angular/core';
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
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = inject(ApiService);
  private readonly TOKEN_KEY = 'soldarte-token';

  get token(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  get usuarioId(): number | null {
    const t = this.token;
    if (!t) return null;
    try {
      return Number(JSON.parse(atob(t.split('.')[1])).sub);
    } catch {
      return null;
    }
  }

  get estaAutenticado(): boolean {
    return !!this.token;
  }

  registro(datos: RegistroData) {
    return this.api.post<UsuarioResponse>('/api/auth/registro', datos);
  }

  login(datos: LoginData) {
    return this.api.post<TokenResponse>('/api/auth/login', datos).pipe(
      tap(res => localStorage.setItem(this.TOKEN_KEY, res.access_token)),
    );
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
  }
}
