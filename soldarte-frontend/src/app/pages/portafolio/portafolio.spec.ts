import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { Portafolio } from './portafolio';
import { PortafolioService } from '../../services/portafolio';

describe('Portafolio', () => {
  let component: Portafolio;
  let fixture: ComponentFixture<Portafolio>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Portafolio],
      providers: [
        {
          provide: PortafolioService,
          useValue: {
            obtenerCategorias: () => of([]),
            obtenerObras: () => of([]),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Portafolio);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
