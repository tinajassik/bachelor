import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from './services/api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class AppComponent implements OnInit {
  title = 'frontend';
  apiResponse: any = null; // ✅ Initialize to avoid undefined errors

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.fetchTest().subscribe(
      data => {
        console.log('API Response:', data);
        this.apiResponse = data; // ✅ Assign response to the variable
      },
      error => {
        console.error('API Error:', error);
      }
    );
  }
}
