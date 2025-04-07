import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  private API_BASE_URL = 'http://127.0.0.1:8000/api/geo/';

  constructor(private http: HttpClient) {}

  fetchTest(): Observable<any> {
    return this.http.get(`${this.API_BASE_URL}test`);
  }

  getStacItemById(stacItemId: string): Observable<any> {
    return this.http.get(this.API_BASE_URL+"item", { params: { item_id: stacItemId }, responseType: 'json' });
  }

  getThumbnailImage(tifUrl:string): Observable<Blob> {
    return this.http.get(this.API_BASE_URL+"thumbnail", {params: {tif_url: tifUrl}, responseType: 'blob' });
  }
}
