import { Component, OnInit } from '@angular/core';
import { SerialService } from './serial.service';

@Component({
  selector: 'app-calibracion',
  templateUrl: './calibracion.component.html',
  styleUrls: ['./calibracion.component.css'],
  
})
export class AppComponent implements OnInit {
  recibido: string[] = [];

  constructor(private serialService: SerialService) {}

  ngOnInit(): void {
    this.getSerial();
    setInterval(() => this.getSerial(), 1000); // Actualiza cada segundo
  }

  getSerial() {
    this.serialService.getSerialData().subscribe(resp => {
      this.recibido = resp.data;
    });
  }
}

