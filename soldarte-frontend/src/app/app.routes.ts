import { Routes } from '@angular/router';
import { Inicio } from './pages/inicio/inicio';
import { Portafolio } from './pages/portafolio/portafolio';
import { Productos } from './pages/productos/productos';
import { Cotizacion } from './pages/cotizacion/cotizacion';
import { Login } from './pages/login/login';
import { Registro } from './pages/registro/registro';
import { Perfil } from './pages/perfil/perfil';
import { Admin } from './pages/admin/admin';
import { AdminProductos } from './pages/admin-productos/admin-productos';
import { AdminPortafolio } from './pages/admin-portafolio/admin-portafolio';
import { AdminCotizaciones } from './pages/admin-cotizaciones/admin-cotizaciones';


export const routes: Routes = [
  { path: '', component: Inicio },
  { path: 'portafolio', component: Portafolio },
  { path: 'productos', component: Productos },
  { path: 'cotizacion', component: Cotizacion },
  { path: 'login', component: Login },
  { path: 'registro', component: Registro },
  { path: 'perfil', component: Perfil },
  { path: 'admin', component: Admin },
  { path: 'admin/productos', component: AdminProductos },
  { path: 'admin/portafolio', component: AdminPortafolio },
  { path: 'admin/cotizaciones', component: AdminCotizaciones },
  { path: '**', redirectTo: '' }
];
