import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { SafeResourceUrl, SafeUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-location',
  imports: [CommonModule],
  templateUrl: './location.component.html',
  styleUrl: './location.component.css',
})
export class LocationComponent {
  @ViewChild('imageRef') imageRef!: ElementRef<HTMLImageElement>;
  @ViewChild('canvasRef') canvasRef!: ElementRef<HTMLCanvasElement>;
  
  @Input() geoCoords: { lat: number; lon: number; mapUrl: SafeResourceUrl} | null = null;
  @Input() error: string | undefined = undefined;
  @Input() loading: boolean = false;
  @Input() imageUrl: SafeUrl | undefined = undefined;

  private resizeObserver: ResizeObserver;
  private point: { originalX: number, originalY: number, imgOriginalWidth: number, imgOriginalHeight: number } | null = null;

  constructor() {
    this.resizeObserver = new ResizeObserver(() => {
      this.updateCanvasSize();
    });
  }

  ngOnDestroy() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  }

  onImageLoad(): void {
    this.updateCanvasSize()
    const img = this.imageRef.nativeElement;
    this.resizeObserver.observe(img)
  }

  drawPoint(originalX: number, originalY: number, imgOriginalHeight: number, imgOriginalWidth: number) {
    this.point = { originalX, originalY, imgOriginalWidth, imgOriginalHeight };
    this.redrawPoint();
  }

  redrawPoint() {
    if(!this.point) return; 

    let { originalX, originalY, imgOriginalHeight, imgOriginalWidth } = this.point;
    originalY = imgOriginalHeight - originalY;
    const canvas = this.canvasRef.nativeElement;
    const ctx = canvas.getContext('2d');
    const img = this.imageRef.nativeElement;

    if (!ctx) return;

    const naturalWidth = imgOriginalWidth;
    const naturalHeight = imgOriginalHeight;

    const displayedWidth = img.clientWidth;
    const displayedHeight = img.clientHeight;

    const scaleX = displayedWidth / naturalWidth;
    const scaleY = displayedHeight / naturalHeight;

    const scaledX = originalX * scaleX;
    const scaledY = originalY * scaleY;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(scaledX, scaledY, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
  }

  private updateCanvasSize() {
    const img = this.imageRef.nativeElement;
    const canvas = this.canvasRef.nativeElement;

    const width = img.clientWidth;
    const height = img.clientHeight;

    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    canvas.width = width;
    canvas.height = height;
    this.redrawPoint();
  }
}