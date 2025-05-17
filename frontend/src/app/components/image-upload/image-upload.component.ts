import { Component } from '@angular/core';
import { BackendApiService } from '../../services/backend-api/backend-api.service';
import { MatListModule } from '@angular/material/list';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { SafeUrl } from '@angular/platform-browser';
import { PredictionsService } from '../../state/predictions.service';
import { MatDialog} from '@angular/material/dialog';
import { ImageModalComponent } from './image-modal/image-modal.component';

@Component({
  selector: 'app-image-upload',
  imports: [
    MatListModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    CommonModule
  ],
  templateUrl: './image-upload.component.html',
  styleUrl: './image-upload.component.css',
})
export class ImageUploadComponent {
  selectedFile: File | null = null;
  detections: any[] = [];
  labeledImageHex: string | null = null;
  filename: string | null = null;
  thumbnailUrl: SafeUrl | undefined = undefined;
  previewUrl: string | null = null;
  statusMessage: string = '';
  statusClass: string = '';

  constructor(
    private backendService: BackendApiService,
    private predictionsService: PredictionsService, private dialog: MatDialog
  ) {}

  onFileSelected(event: any) {
    const fileInput = event.target as HTMLInputElement;
    this.thumbnailUrl = '';
    this.statusMessage = '';
    this.statusClass = '';

    if (fileInput.files && fileInput.files.length > 0) {
      this.selectedFile = fileInput.files[0];
      this.statusMessage = 'Image loaded successfully!';
      this.statusClass = 'success';
      this.showPreview()
      
      const stacId = this.extractStacIdFromFilename(this.selectedFile.name);
      if (!stacId) {
        this.statusMessage = 'Failed to extract STAC ID from filename.';
        this.statusClass = 'error';
        return;
      }

    this.backendService.getStacItemById(stacId).subscribe({
      next: (result) => {
        const tifUrl = result.assets?.data?.href || null;

        if (!tifUrl) {
          this.statusMessage = 'No data asset found in STAC item.';
          this.statusClass = 'error';
          return;
        }

        this.backendService.getThumbnailImage(tifUrl).subscribe({
          next: (blob) => {
            this.thumbnailUrl = URL.createObjectURL(blob);
          },
          error: (err) => {
            this.statusMessage = 'Failed to load thumbnail image.';
            this.statusClass = 'error';
            console.error("Thumbnail error:", err.message);
          }
        });
      },
      error: (err) => {
        this.statusMessage = 'Failed to fetch STAC metadata.';
        this.statusClass = 'error';
        console.error("STAC error:", err.message);
      }
    });
    } else {
      this.statusMessage = 'No file selected.';
      this.statusClass = 'error';
    }
  }

  onDetect(): void {
    if (!this.selectedFile) {
      this.statusMessage = 'Please upload an image before running detection.';
      this.statusClass = 'error';
      return;
    }
  
    this.statusMessage = 'Detecting cars...';
    this.statusClass = 'loading';
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
  
    this.backendService.detectCars(formData).subscribe({
      next: (response) => {
        this.filename = response.filename;
        this.labeledImageHex = response.labeled_image;

        const coords = response.projected_geolocations.geolocations;
        this.detections = response.detections.map((det: any, i: number) => ({
          ...det,
          geographic_coords: coords[i] ?? null
        }));

        this.predictionsService.setLabeledImageSrc(this.labeledImageHex!);
        this.predictionsService.setMapUrl(response.projected_geolocations.map_url);
        this.predictionsService.setDetections(this.detections);
  
        this.statusMessage = 'Detection completed successfully!';
        this.statusClass = 'success';
      },
      error: (error) => {
        console.error('Detection error:', error.message);
        this.statusMessage = 'An error occurred during detection: ' + error.message;
        this.statusClass = 'error';
      }
    });
  }

  openImageModal(): void {
    if (this.previewUrl) {
      this.dialog.open(ImageModalComponent, {
        data: { imageUrl: this.previewUrl },
        width: '90vw',
        maxHeight: '90vh',
        panelClass: 'custom-dialog-container'
      });
    }
  }
  openThumbnailModal(): void {
    if (this.thumbnailUrl) {
      this.dialog.open(ImageModalComponent, {
        data: { imageUrl: this.thumbnailUrl },
        width: '90vw',
        maxHeight: '90vh',
        panelClass: 'custom-dialog-container'
      });
    }
  }

  private extractStacIdFromFilename(filename: string): string {
    const index = filename.indexOf('-');
    return index !== -1 ? filename.substring(0, index) : filename;
  }

  private showPreview() {
    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
    };
    reader.readAsDataURL(this.selectedFile!);
  }
}
