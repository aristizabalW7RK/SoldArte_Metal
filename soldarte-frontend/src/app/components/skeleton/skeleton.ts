import { Component, input, computed } from '@angular/core';

@Component({
  selector: 'app-skeleton',
  template: `
    @switch (tipo()) {
      @case ('card-grid') {
        <div class="sk-grid" [style.--cols]="columnas()">
          @for (_ of items(); track $index) {
            <div class="sk-card">
              <div class="sk-img"></div>
              <div class="sk-line" style="width: 70%"></div>
              <div class="sk-line" style="width: 45%"></div>
              <div class="sk-line" style="width: 90%"></div>
            </div>
          }
        </div>
      }
      @case ('chip') {
        <div class="sk-chips">
          @for (_ of items(); track $index) {
            <div class="sk-chip"></div>
          }
        </div>
      }
      @case ('card-list') {
        <div class="sk-list">
          @for (_ of items(); track $index) {
            <div class="sk-card-list">
              <div class="sk-line" style="width: 55%"></div>
              <div class="sk-line" style="width: 85%"></div>
              <div class="sk-line" style="width: 75%"></div>
              <div class="sk-line" style="width: 40%"></div>
              <div class="sk-line" style="width: 30%"></div>
            </div>
          }
        </div>
      }
      @case ('fila') {
        <div class="sk-list">
          @for (_ of items(); track $index) {
            <div class="sk-fila">
              <div class="sk-thumb"></div>
              <div class="sk-line" style="width: 40%"></div>
              <div class="sk-line" style="width: 20%; margin-left: auto;"></div>
            </div>
          }
        </div>
      }
    }
  `,
  styles: `
    .sk-grid, .sk-list, .sk-chips { display: flex; }
    .sk-grid {
      display: grid;
      grid-template-columns: repeat(var(--cols, 3), 1fr);
      gap: 1.5rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .sk-list { flex-direction: column; gap: 1rem; }
    .sk-chips { flex-wrap: wrap; gap: 0.75rem; justify-content: center; padding: 1.5rem 0 3rem; }

    .sk-card, .sk-card-list, .sk-fila {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 4px;
      overflow: hidden;
    }

    .sk-card { padding: 0; }
    .sk-card-list { padding: 1.2rem; display: flex; flex-direction: column; gap: 0.6rem; }
    .sk-fila {
      padding: 0.8rem;
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }

    .sk-img {
      width: 100%;
      aspect-ratio: 16 / 10;
      background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-card) 50%, var(--bg-secondary) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    .sk-chip {
      width: 90px;
      height: 36px;
      border-radius: 4px;
      background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-secondary) 50%, var(--bg-card) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    .sk-line {
      height: 12px;
      border-radius: 4px;
      margin: 0.2rem 0.5rem;
      background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-card) 50%, var(--bg-secondary) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    .sk-card .sk-line {
      margin: 0.5rem 0.8rem;
    }

    .sk-thumb {
      width: 50px;
      height: 50px;
      border-radius: 6px;
      flex-shrink: 0;
      background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-card) 50%, var(--bg-secondary) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    @keyframes shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }

    @media (max-width: 1024px) {
      .sk-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
      .sk-grid { grid-template-columns: 1fr; }
    }
  `,
})
export class SkeletonComponent {
  tipo = input<'card-grid' | 'chip' | 'card-list' | 'fila'>('card-grid');
  cantidad = input(4);
  columnas = input(3);
  items = computed(() => Array.from({ length: this.cantidad() }, (_, i) => i));
}
