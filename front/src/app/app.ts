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
  constructor(private http: HttpClient) { }
  autoCalibrar() {
    this.http.post('http://127.0.0.1:8000/serial', { data: this.comando })
      .subscribe({
        next: () => alert('Comando enviado correctamente'),
        error: () => alert('Error al enviar el comando')
      });
  }
}

