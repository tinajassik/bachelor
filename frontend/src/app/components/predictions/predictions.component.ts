import { Component, Input } from '@angular/core';
import { MapComponent } from '../map/map.component';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { PredictionsService } from '../../state/predictions.service';
import { DetectionsListComponent } from './detections-list/detections-list.component';

@Component({
  selector: 'app-predictions',
  imports: [MapComponent, CommonModule, DetectionsListComponent],
  templateUrl: './predictions.component.html'
})
export class PredictionsComponent {
  geoCoords: { lat: number; lon: number; mapUrl: SafeResourceUrl} | null = null;
  error: string | undefined = undefined;
  labeledImageSrc: string | undefined = undefined;

  constructor(private predictionsService: PredictionsService, private sanitizer: DomSanitizer) {}

  ngOnInit() {
    this.predictionsService.getLabeledImageSrc().subscribe(imageSrc => {
      this.labeledImageSrc = imageSrc;
    })
    this.predictionsService.getMapUrl().subscribe(mapUrl => {
     this.geoCoords =  { lat: 0, lon: 0, mapUrl: this.sanitizer.bypassSecurityTrustResourceUrl(mapUrl)}; 
    })
  }
}
