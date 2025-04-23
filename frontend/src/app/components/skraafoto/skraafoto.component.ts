import { Component } from '@angular/core';
import { MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { BackendApiService } from '../../services/backend-api/backend-api.service';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-skraafoto',
  imports: [MatInputModule, MatButtonModule, FormsModule, CommonModule],
  templateUrl: './skraafoto.component.html',
  styleUrl: './skraafoto.component.css'
})

export class SkraafotoComponent {

  stacItemId: string | null = null;
  imageUrl: SafeUrl | null = null;
  loading: boolean = false;
  error: string | null = null;
  pixelX: number | null = null;
  pixelY: number | null = null;
  geoCoords: { lat: number; lon: number; mapUrl: SafeResourceUrl} | null = null;

  constructor(private backendService: BackendApiService, private sanitizer: DomSanitizer) {

  }

  onFetch() {
    this.loading = true;
    this.error = null;
    this.imageUrl = null;

    this.backendService.getStacItemById(this.stacItemId!).subscribe({
      next: (result) => {
        const tifUrl = result.assets?.data?.href || null;
        if (!tifUrl) {
          this.error = 'No image found for this STAC item.';
          this.loading = false;
          return;
        }

        this.backendService.getThumbnailImage(tifUrl).subscribe({
          next: (blob) => {
            const objectURL = URL.createObjectURL(blob);
            this.imageUrl = objectURL;
            this.loading = false;
          },
          error: (err) => {
            this.error = 'Failed to fetch image.' + err.message;
            this.loading = false;
          }
        });
      },
      error: (err) => {
        this.error = 'Failed to fetch item. Please check the ID.' + err.message;
        this.loading = false;
      }
    })
  }

  onGetGeoLocation() {
    if (this.pixelX === null || this.pixelY === null || this.stacItemId === null) return;
    this.geoCoords = null;

    this.backendService.getGeoLocation(this.stacItemId, this.pixelX, this.pixelY).subscribe({
      next: (result) => {
        this.geoCoords = { lat: result.latitude, lon: result.longitude, mapUrl: this.sanitizer.bypassSecurityTrustResourceUrl(result.map_url)};
      },
      error: (err) => {
        this.error = err.error.detail;
      }
    })

  }
}
