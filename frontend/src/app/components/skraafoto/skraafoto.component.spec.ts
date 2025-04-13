import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkraafotoComponent } from './skraafoto.component';
import { provideHttpClient } from '@angular/common/http';
import { BackendApiService } from '../../services/backend-api/backend-api.service';

describe('SkraafotoComponent', () => {
  let component: SkraafotoComponent;
  let fixture: ComponentFixture<SkraafotoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkraafotoComponent],
      providers: [
        provideHttpClient(),
        BackendApiService,
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkraafotoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
