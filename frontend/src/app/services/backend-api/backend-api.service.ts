import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {
  private API_BASE_URL = 'http://127.0.0.1:8000/';

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

  getFullImage(stacItemId: string): Observable<any> {
    return this.http.get(this.API_BASE_URL+"image", {params: { item_id: stacItemId }, responseType: 'blob'});
  }

  getGeoLocation(stacItemId: string, pixelX: number, pixelY: number): Observable<any> {
    return this.http.get(this.API_BASE_URL+"location", {params: {item_id: stacItemId, pixel_x: pixelX, pixel_y: pixelY}, responseType: 'json'});
  }

  getAvailableStacItems(): Observable<any> {
    return this.http.get(this.API_BASE_URL+"items", {params: {responseType: 'json'}});
  }

  detectCars(file: FormData): Observable<any> {
    return this.http.post<any>(this.API_BASE_URL +"detect", file);
  }

}
