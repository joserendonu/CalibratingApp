import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SerialService {
  private apiUrl = 'http://localhost:8000/serial';

  constructor(private http: HttpClient) {}

  getSerialData(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  sendSerialData(data: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { data });
  }
}