import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http } from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { CompanyService } from './company.service';

describe('CompanyService', () => {
	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [
				CompanyService,
				{
					provide: Http, useFactory: (backend, options) => {
						return new Http(backend, options);
					},
					deps: [MockBackend, BaseRequestOptions]
				},
				MockBackend,
				BaseRequestOptions
			]
		});
	});

	it('should ...', inject([CompanyService], (service: CompanyService) => {
		expect(service).toBeTruthy();
	}));
});
