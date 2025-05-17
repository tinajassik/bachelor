import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetectionsListComponent } from './detections-list.component';

describe('DetectionsListComponent', () => {
  let component: DetectionsListComponent;
  let fixture: ComponentFixture<DetectionsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DetectionsListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DetectionsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
