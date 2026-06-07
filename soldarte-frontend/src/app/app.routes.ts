import { Routes } from '@angular/router';
import { Inicio } from './pages/inicio/inicio';
import { Portafolio } from './pages/portafolio/portafolio';
import { Productos } from './pages/productos/productos';
import { Cotizacion } from './pages/cotizacion/cotizacion';
import { Login } from './pages/login/login';
import { Registro } from './pages/registro/registro';


export const routes: Routes = [
  { path: '', component: Inicio },
  { path: 'portafolio', component: Portafolio },
  { path: 'productos', component: Productos },
  { path: 'cotizacion', component: Cotizacion },
  { path: 'login', component: Login },
  { path: 'registro', component: Registro },
  { path: '**', redirectTo: '' }    
];