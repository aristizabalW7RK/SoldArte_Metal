import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  readonly baseUrl = environment.apiUrl;
  private readonly TOKEN_KEY = 'soldarte-token';

  private get authHeaders(): Record<string, string> {
    const token = localStorage.getItem(this.TOKEN_KEY);
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  get<T>(path: string, params?: Record<string, string>) {
    return this.http.get<T>(`${this.baseUrl}${path}`, { params });
  }

  post<T>(path: string, body: unknown) {
    return this.http.post<T>(`${this.baseUrl}${path}`, body, { headers: this.authHeaders });
  }

  put<T>(path: string, body: unknown) {
    return this.http.put<T>(`${this.baseUrl}${path}`, body, { headers: this.authHeaders });
  }

  patch<T>(path: string, body: unknown) {
    return this.http.patch<T>(`${this.baseUrl}${path}`, body, { headers: this.authHeaders });
  }

  delete<T>(path: string) {
    return this.http.delete<T>(`${this.baseUrl}${path}`, { headers: this.authHeaders });
  }
}
