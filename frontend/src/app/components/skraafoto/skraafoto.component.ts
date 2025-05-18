import { Component, ViewChild } from '@angular/core';
import { MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { BackendApiService } from '../../services/backend-api/backend-api.service';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { LocationComponent } from './location/location.component';

@Component({
  selector: 'app-skraafoto',
  imports: [MatInputModule, MatButtonModule, FormsModule, CommonModule, MatAutocompleteModule, LocationComponent],
  templateUrl: './skraafoto.component.html',
  styleUrl: './skraafoto.component.css'
})

export class SkraafotoComponent {
  stacItemId: string | null = null;
  imageUrl: SafeUrl | undefined = undefined;
  thumbnailUrl: SafeUrl | undefined = undefined;
  loading: boolean = false;
  error: string | undefined = undefined;
  pixelX: number | null = null;
  pixelY: number | null = null;
  geoCoords: { lat: number; lon: number; mapUrl: SafeResourceUrl} | null = null;
  availableStacItems: string[] = [];
  imgOriginalWidth: number = 0;
  imgOriginalHeight: number = 0;
  @ViewChild(LocationComponent) locationComponent!: LocationComponent;

  constructor(private backendService: BackendApiService, private sanitizer: DomSanitizer) {

  }

  ngOnInit() {
    this.backendService.getAvailableStacItems().subscribe({
      next: result => this.availableStacItems = result,
      error: err => this.error = err.error.detail
    } );
  }

  onFetch() {
    this.loading = true;
    this.error = undefined;
    this.imageUrl = undefined;

    this.backendService.getStacItemById(this.stacItemId!).subscribe({
      next: (result) => {
        console.log('Data received from getStacItemById:', result); // <-- Added this log
        const tifUrl = result.assets?.data?.href || null;
        this.imgOriginalHeight = result.properties['proj:shape'][0];
        this.imgOriginalWidth = result.properties['proj:shape'][1];
        if (!tifUrl) {
          this.error = 'No image found for this STAC item.';
          this.loading = false;
          return;
        }

        this.backendService.getThumbnailImage(tifUrl!).subscribe({
          next: (blob) => {
            const objectURL = URL.createObjectURL(blob);
            this.thumbnailUrl = objectURL;
          },
          error: (err) => {
            console.log("Failed to display image thumbnail: ", err.message)
          }
        });

        this.backendService.getFullImage(this.stacItemId!).subscribe({
          next: (blob) => {
            const objectURL = URL.createObjectURL(blob);
            this.imageUrl = objectURL;
            this.loading = false;
          },
          error: (err) => {
            this.error = 'Failed to fetch image.' + err.error.detail;
            this.loading = false;
          }
        });
      },
      error: (err) => {
        console.error('Error from getStacItemById subscription:', err); // <-- Added this log
        this.error = 'Failed to fetch item. Please check the ID.' + err.error.detail;
        this.loading = false;
      }
    })
  }

  onGetGeoLocation() {
    if (this.pixelX === null || this.pixelY === null || this.stacItemId === null) return;
    this.geoCoords = null;
    this.error = undefined;
    this.locationComponent.drawPoint(this.pixelX, this.pixelY,this.imgOriginalHeight, this.imgOriginalWidth)
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
