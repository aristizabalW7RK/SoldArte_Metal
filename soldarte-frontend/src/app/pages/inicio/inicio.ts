import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TemaService } from '../../services/tema';

@Component({
  selector: 'app-inicio',
  imports: [RouterLink],
  templateUrl: './inicio.html',
  styleUrl: './inicio.css',
})
export class Inicio {
  constructor(public temaService: TemaService) {}
}
