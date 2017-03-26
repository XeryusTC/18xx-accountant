import { TestBed, inject } from '@angular/core/testing';

import { CompanyService } from './company.service';

describe('CompanyServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CompanyService]
    });
  });

  it('should ...', inject([CompanyService], (service: CompanyService) => {
    expect(service).toBeTruthy();
  }));
});
