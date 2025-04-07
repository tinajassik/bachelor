import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkraafotoComponent } from './skraafoto.component';

describe('SkraafotoComponent', () => {
  let component: SkraafotoComponent;
  let fixture: ComponentFixture<SkraafotoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkraafotoComponent]
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
