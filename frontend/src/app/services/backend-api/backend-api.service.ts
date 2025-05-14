import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  // Now that Nginx is proxying, the frontend calls its own origin
  // and Nginx forwards requests starting with /api/
  // The actual backend URL (http://127.0.0.1:8000/) is now effectively hidden from the browser.
  private API_BASE_URL = '/api/'; // This assumes your backend routes (like /item) don't already start with /api

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
