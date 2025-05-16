import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagesDownloadComponent } from './images-download.component';
import { provideHttpClient } from '@angular/common/http';
import { BackendApiService } from '../services/backend-api/backend-api.service';

describe('ImagesDownloadComponent', () => {
  let component: ImagesDownloadComponent;
  let fixture: ComponentFixture<ImagesDownloadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImagesDownloadComponent],
      providers: [
        provideHttpClient(),
        BackendApiService,
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImagesDownloadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
