import { TestBed } from '@angular/core/testing';

import { BackendApiService } from './backend-api.service';
import { provideHttpClient } from '@angular/common/http';

describe('BackendApiService', () => {
  let service: BackendApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({providers: [provideHttpClient()]});
    service = TestBed.inject(BackendApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
