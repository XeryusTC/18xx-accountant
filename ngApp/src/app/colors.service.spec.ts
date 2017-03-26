import { TestBed, inject } from '@angular/core/testing';

import { ColorsService } from './colors.service';

describe('ColorsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ColorsService]
    });
  });

  it('should ...', inject([ColorsService], (service: ColorsService) => {
    expect(service).toBeTruthy();
  }));
});
