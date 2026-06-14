import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TemaService } from '../../services/tema';

@Component({
  selector: 'app-footer',
  imports: [RouterLink],
  templateUrl: './footer.html',
  styleUrl: './footer.css',
})
export class Footer {
  temaService = inject(TemaService);
}
