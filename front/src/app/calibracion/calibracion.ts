import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
// ...
@Component({
  selector: 'app-calibracion',
  standalone: true,
  imports: [FormsModule, HttpClientModule], // <-- AGREGA ESTO

  templateUrl: './calibracion.component.html',
  styleUrls: ['./calibracion.component.css']
})
export class CalibracionComponent {


  enviarSalida() {
    this.http.post('http://127.0.0.1:8000/serial', { data: this.salida })
      .subscribe({
        next: () => alert('Enviado correctamente'),
        error: () => alert('Error al enviar')
      });
  }
  escala = 0;
  escala2 = 0;
  peso = 0;
  pesoPatron = 5.0;
  salida = '';


  constructor(private http: HttpClient) {}

  setEscala() {
    // lógica para setear escala
  }

  setCero() {
    // lógica para setear cero
  }

  autoCalibrar() {
    // lógica para auto calibrar
  }

}
