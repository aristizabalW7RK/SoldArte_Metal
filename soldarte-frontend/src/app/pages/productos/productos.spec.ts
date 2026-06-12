import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { Productos } from './productos';
import { ProductoService } from '../../services/productos';

describe('Productos', () => {
  let component: Productos;
  let fixture: ComponentFixture<Productos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Productos],
      providers: [
        {
          provide: ProductoService,
          useValue: {
            obtenerProductos: () => of([]),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Productos);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
