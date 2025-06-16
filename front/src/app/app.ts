import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, RouterOutlet, HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected title = 'front';
  comando = '';
  nuevaEscala: number = 103; // Valor por defecto
  constructor(private http: HttpClient) { }
  autoCalibrar() {
    this.http.post('http://127.0.0.1:8000/serial', { data: this.comando })
      .subscribe({
        next: () => alert('Comando enviado correctamente'),
        error: () => alert('Error al enviar el comando')
      });
  }
  enviarConfiguracion() {
    this.http.post('http://127.0.0.1:8000/serial', { data: 'config' })
      .subscribe({
        next: () => alert('Comando CONFIG enviado correctamente'),
        error: () => alert('Error al enviar el comando CONFIG')
      });
  }
  enviarAuto() {
    this.http.post('http://127.0.0.1:8000/serial', { data: 'auto' })
      .subscribe({
        next: () => alert('Comando AUTO enviado correctamente'),
        error: () => alert('Error al enviar el comando AUTO')
      });
  }
  cambiarEscala() {
    const comando = `setScale ${this.nuevaEscala}`;

    this.http.post('http://127.0.0.1:8000/serial', { data: comando })
      .subscribe({
        next: () => alert(`Escala enviada correctamente: ${this.nuevaEscala}`),
        error: () => alert('Error al enviar el comando de escala')
      });
  }
}

