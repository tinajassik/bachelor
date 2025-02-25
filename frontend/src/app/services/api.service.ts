import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private API_BASE_URL = 'http://127.0.0.1:8000/api/skraafoto';

  constructor(private http: HttpClient) {}

  fetchTest(): Observable<any> {
    return this.http.get(`${this.API_BASE_URL}/test`);
  }

  fetchImage(imageUrl: string): Observable<Blob> {
    return this.http.get(imageUrl, { responseType: 'blob' });
  }
}
