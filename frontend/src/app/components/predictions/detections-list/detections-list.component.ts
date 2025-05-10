import { Component } from '@angular/core';
import { PredictionsService } from '../../../state/predictions.service';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule} from '@angular/material/expansion'

@Component({
  selector: 'app-detections-list',
  imports: [CommonModule, MatListModule, MatExpansionModule],
  templateUrl: './detections-list.component.html',
  styleUrl: './detections-list.component.css'
})
export class DetectionsListComponent {
  detections: any[] = [];

  constructor(private predictionsService: PredictionsService) {}

  ngOnInit(): void {
    this.predictionsService.getDetections().subscribe((data: any[]) => {
      this.detections = data;
    });
  }
}
