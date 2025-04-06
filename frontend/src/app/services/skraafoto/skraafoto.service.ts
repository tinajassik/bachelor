import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SkraafotoService {

  private API_BASE_URL: string = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/"

  constructor(private http: HttpClient) { }

  getStacItemById(stacIdemId: string): Observable<any> {
      return this.http.get(this.API_BASE_URL+"collections/skraafotos2023/items/"+stacIdemId, { responseType: 'json' });
  }
}
