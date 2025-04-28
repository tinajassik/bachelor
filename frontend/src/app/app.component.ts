import { Component } from '@angular/core';
import { BackendApiService } from './services/backend-api/backend-api.service';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';

@Component({
  selector: 'app-root',
  imports: [CommonModule, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  responseTest =  undefined;

  constructor(private backendApiService: BackendApiService){}


  ngOnInit() {
    this.backendApiService.fetchTest().subscribe(r => {
      this.responseTest = r.message
    })
  }
}
