import { TestBed } from '@angular/core/testing';

import { SkraafotoService } from './skraafoto.service';
import { provideHttpClient } from '@angular/common/http';

describe('SkraafotoService', () => {
  let service: SkraafotoService;

  beforeEach(() => {
    TestBed.configureTestingModule({providers: [provideHttpClient()
    ]});
    service = TestBed.inject(SkraafotoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
