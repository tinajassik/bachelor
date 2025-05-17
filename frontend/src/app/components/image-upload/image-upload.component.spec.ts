import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageUploadComponent } from './image-upload.component';
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { of } from 'rxjs';

describe('ImageUploadComponent', () => {
  let component: ImageUploadComponent;
  let fixture: ComponentFixture<ImageUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImageUploadComponent],
      providers: [provideHttpClient()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImageUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should handle file selection and set preview', () => {
    const file = new File(['fake content'], 'test-image-1234567890.png', { type: 'image/png' });
    const event = { target: { files: [file] } };
  
    spyOn<any>(component, 'showPreview'); // spy since it's private
    spyOn(component as any, 'extractStacIdFromFilename').and.returnValue('test-id');
  
    component.onFileSelected(event);
  
    expect(component.selectedFile).toBe(file);
    expect(component.statusMessage).toBe('Image loaded successfully!');
    expect(component.statusClass).toBe('success');
    expect((component as any).showPreview).toHaveBeenCalled();
  });

  it('should handle no file selected', () => {
    const event = { target: { files: [] } };
    component.onFileSelected(event);
    expect(component.statusMessage).toBe('No file selected.');
    expect(component.statusClass).toBe('error');
  });

  it('should show error when STAC ID cannot be extracted', () => {
    const file = new File(['test'], 'badname', { type: 'image/png' });
    const event = { target: { files: [file] } };
  
    spyOn(component as any, 'extractStacIdFromFilename').and.returnValue('');
  
    component.onFileSelected(event);
  
    expect(component.statusMessage).toBe('Failed to extract STAC ID from filename.');
    expect(component.statusClass).toBe('error');
  });  

  it('should open image modal with preview image', () => {
    const dialogSpy = spyOn(component['dialog'], 'open');
    component.previewUrl = 'data:image/png;base64,some-fake-data';
  
    component.openImageModal();
  
    expect(dialogSpy).toHaveBeenCalledWith(jasmine.any(Function), jasmine.objectContaining({
      data: { imageUrl: component.previewUrl }
    }));
  });
  it('should open image modal with thumbnail', () => {
    const dialogSpy = spyOn(component['dialog'], 'open');
    component.thumbnailUrl = 'blob:http://localhost/fake-id';
  
    component.openThumbnailModal();
  
    expect(dialogSpy).toHaveBeenCalledWith(jasmine.any(Function), jasmine.objectContaining({
      data: { imageUrl: component.thumbnailUrl }
    }));
  });

  it('should set detections and update predictionsService on successful detect', () => {
    const file = new File(['test'], 'file-1234.png');
    component.selectedFile = file;
  
    const mockResponse = {
      filename: 'result.png',
      labeled_image: 'abcd1234',
      detections: [
        { class_id: 1, confidence: 0.9, bbox: [0, 0, 10, 10] }
      ],
      projected_geolocations: {
        geolocations: [[14.123456, 55.123456]],
        map_url: 'http://map.url'
      }
    };
  
    spyOn(component['backendService'], 'detectCars').and.returnValue(of(mockResponse));
  
    const predSpy = component['predictionsService'];
    spyOn(predSpy, 'setLabeledImageSrc');
    spyOn(predSpy, 'setMapUrl');
    spyOn(predSpy, 'setDetections');
  
    component.onDetect();
  
    expect(component.filename).toBe('result.png');
    expect(component.detections.length).toBe(1);
    expect(component.statusClass).toBe('success');
    expect(predSpy.setDetections).toHaveBeenCalledWith(jasmine.any(Array));
  });  
  
});
