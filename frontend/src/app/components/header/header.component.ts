import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from  '@angular/material/tabs'
import { SkraafotoComponent } from '../skraafoto/skraafoto.component';
import { ImageUploadComponent } from '../image-upload/image-upload.component';
import { PredictionsComponent } from '../predictions/predictions.component';
import { ImagesDownloadComponent } from '../../images-download/images-download.component';


@Component({
  selector: 'app-header',
  imports: [MatToolbarModule, MatTabsModule, SkraafotoComponent, ImageUploadComponent, PredictionsComponent, ImagesDownloadComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

}
