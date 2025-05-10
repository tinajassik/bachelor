import { CommonModule } from '@angular/common';
import { SafeResourceUrl } from '@angular/platform-browser';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-map',
  imports: [CommonModule],
  templateUrl: './map.component.html',
  styleUrl: './map.component.css'
})
export class MapComponent {
  @Input() geoCoords: { lat: number; lon: number; mapUrl: SafeResourceUrl} | null = null;
}
