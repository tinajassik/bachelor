import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from  '@angular/material/tabs'
import { SkraafotoComponent } from '../skraafoto/skraafoto.component';

@Component({
  selector: 'app-header',
  imports: [MatToolbarModule, MatTabsModule, SkraafotoComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

}
