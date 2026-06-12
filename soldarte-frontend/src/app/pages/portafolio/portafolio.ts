import { Component, inject, signal, computed } from '@angular/core';
import { PortafolioService, Categoria, Obra } from '../../services/portafolio';

@Component({
  selector: 'app-portafolio',
  imports: [],
  templateUrl: './portafolio.html',
  styleUrl: './portafolio.css',
})
export class Portafolio {
  private portafolioService = inject(PortafolioService);

  categorias = signal<Categoria[]>([]);
  obras = signal<Obra[]>([]);
  categoriaSeleccionada = signal<number | null>(null);
  cargando = signal(true);

  obrasFiltradas = computed(() => {
    const catId = this.categoriaSeleccionada();
    if (!catId) return this.obras();
    return this.obras().filter(o => o.categoria_id === catId);
  });

  constructor() {
    this.portafolioService.obtenerCategorias().subscribe(cats => {
      this.categorias.set(cats);
    });
    this.portafolioService.obtenerObras().subscribe(obras => {
      this.obras.set(obras);
      this.cargando.set(false);
    });
  }

  filtrarPorCategoria(id: number | null) {
    this.categoriaSeleccionada.set(id);
  }
}
