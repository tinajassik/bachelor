import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { SafeUrl } from '@angular/platform-browser';
import { BackendApiService } from '../../services/backend-api/backend-api.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-images-download',
  imports: [MatInputModule, MatButtonModule, FormsModule, CommonModule, MatAutocompleteModule, MatProgressSpinnerModule],
  templateUrl: './images-download.component.html',
  styleUrl: './images-download.component.css'
})
export class ImagesDownloadComponent {

stacItemId: string | null = null;
  imageUrl: SafeUrl | undefined = undefined;
  thumbnailUrl: SafeUrl | undefined = undefined;
  loading: boolean = false;
  error: string | undefined = undefined;
  downloading = false;
  availableStacItems: string[] = [];
  imgOriginalWidth: number = 0;
  imgOriginalHeight: number = 0;

  constructor(private backendService: BackendApiService) {
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
        const tifUrl = result.assets?.data?.href || null;
        this.imgOriginalHeight = result.properties['proj:shape'][0];
        this.imgOriginalWidth = result.properties['proj:shape'][1];
        this.loading = false;
        if (!tifUrl) {
          this.error = 'No image found for this STAC item.';
          return;
        }

        this.backendService.getThumbnailImage(tifUrl!).subscribe({
          next: (blob) => {
            const objectURL = URL.createObjectURL(blob);
            this.thumbnailUrl = objectURL;
            this.loading = false;
          },
          error: (err) => {
            console.log("Failed to display image thumbnail: ", err.message)
          }
        });
      },
      error: (err) => {
        this.error = 'Failed to fetch item. Please check the ID.' + err.error.detail;
        this.loading = false;
      }
    })
  }

  onDownload() {
    if (!this.stacItemId) {
    this.error = 'STAC Item ID is required.';
    return;
  }

  this.downloading = true;
  this.backendService.getCroppedImages(this.stacItemId).subscribe({
    next: (blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.stacItemId}_cropped_images.zip`;
      a.click();
      this.downloading = false;
      window.URL.revokeObjectURL(url); 
    },
    error: (err) => {
      this.downloading = false;
      this.error = 'Failed to download cropped images: ' + (err.error?.detail || err.message);
    }
  });
  }
}
