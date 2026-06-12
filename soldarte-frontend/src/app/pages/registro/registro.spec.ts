import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { provideRouter } from '@angular/router';

import { Registro } from './registro';
import { AuthService } from '../../services/auth';

describe('Registro', () => {
  let component: Registro;
  let fixture: ComponentFixture<Registro>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Registro],
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: {
            registro: () => of({ id: 1, nombre: 'Test', email: 'test@test.com', telefono: null, created_at: '' }),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Registro);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
