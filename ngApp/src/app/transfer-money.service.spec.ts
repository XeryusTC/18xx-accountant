import { TestBed, inject } from '@angular/core/testing';

import { TransferMoneyService } from './transfer-money.service';

describe('TransferMoneyService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TransferMoneyService]
    });
  });

  it('should ...', inject([TransferMoneyService], (service: TransferMoneyService) => {
    expect(service).toBeTruthy();
  }));
});
