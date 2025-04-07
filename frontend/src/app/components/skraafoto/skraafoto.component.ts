import { Component } from '@angular/core';
import { MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { BackendApiService } from '../../services/backend-api/backend-api.service';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-skraafoto',
  imports: [MatInputModule, MatButtonModule, FormsModule, CommonModule],
  templateUrl: './skraafoto.component.html',
  styleUrl: './skraafoto.component.css'
})

export class SkraafotoComponent {

  stacItemId: string | undefined = undefined;
  imageUrl: SafeUrl | null = null;
  loading: boolean = false;
  error: string | null = null;

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
}
