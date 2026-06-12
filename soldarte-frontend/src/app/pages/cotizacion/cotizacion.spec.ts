import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { Cotizacion } from './cotizacion';
import { CotizacionService } from '../../services/cotizacion';
import { TemaService } from '../../services/tema';
import { AuthService } from '../../services/auth';

describe('Cotizacion', () => {
  let component: Cotizacion;
  let fixture: ComponentFixture<Cotizacion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Cotizacion],
      providers: [
        {
          provide: CotizacionService,
          useValue: {
            crear: () => of({ id: 1, nombre_cliente: 'Test', telefono: '123', email: 't@t.com', tipo_trabajo: 'reja', descripcion: 'test', direccion: null, estado: 'nueva', created_at: '' }),
          },
        },
        TemaService,
        {
          provide: AuthService,
          useValue: { usuarioId: null },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Cotizacion);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
