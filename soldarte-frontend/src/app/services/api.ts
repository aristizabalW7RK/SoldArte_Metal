import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  readonly baseUrl = environment.apiUrl;

  private get options() {
    return { withCredentials: true };
  }

  get<T>(path: string, params?: Record<string, string>) {
    return this.http.get<T>(`${this.baseUrl}${path}`, { ...this.options, params });
  }

  post<T>(path: string, body: unknown) {
    return this.http.post<T>(`${this.baseUrl}${path}`, body, this.options);
  }

  put<T>(path: string, body: unknown) {
    return this.http.put<T>(`${this.baseUrl}${path}`, body, this.options);
  }

  patch<T>(path: string, body: unknown) {
    return this.http.patch<T>(`${this.baseUrl}${path}`, body, this.options);
  }

  delete<T>(path: string) {
    return this.http.delete<T>(`${this.baseUrl}${path}`, this.options);
  }
}
