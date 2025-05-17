import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageModalComponent } from './image-modal.component';
import { MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

describe('ImageModalComponent', () => {
  let component: ImageModalComponent;
  let fixture: ComponentFixture<ImageModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImageModalComponent], 
      providers: [
        {
          provide: MAT_DIALOG_DATA,
          useValue: { imageUrl: 'mock-image.png' }
        },
        {
          provide: MatDialogRef,
          useValue: {}
        }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImageModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render image with the correct src', () => {
    const imgElement: HTMLImageElement = fixture.nativeElement.querySelector('img');
    expect(imgElement).toBeTruthy();
    expect(imgElement.src).toContain('mock-image.png');
  });
});
