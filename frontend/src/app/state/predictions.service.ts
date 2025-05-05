import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionsService {
  private labeledImageSrc = new Subject<string>;
  private mapUrl = new Subject<string>;
  private detections = new Subject<any[]>();
  
  constructor() { }

  setLabeledImageSrc(labeledImageHex: string) {
    this.labeledImageSrc.next(labeledImageHex ? 'data:image/png;base64,' + btoa(this.hexToBinary(labeledImageHex)): '');
  }

  getLabeledImageSrc(): Observable<string>{
    return this.labeledImageSrc.asObservable();
  }

  setMapUrl(mapUrl: string) {
    this.mapUrl.next(mapUrl);
  }

  getMapUrl(): Observable<string>{
    return this.mapUrl.asObservable();
  }

  setDetections(detections: any[]) {
    this.detections.next(detections);
  }
  
  getDetections(): Observable<any[]> {
    return this.detections.asObservable();
  }

  private hexToBinary(hex: string): string {
    const bytes = [];
    for (let i = 0; i < hex.length; i += 2) {
      bytes.push(String.fromCharCode(parseInt(hex.substr(i, 2), 16)));
    }
    return bytes.join('');
  }
}
