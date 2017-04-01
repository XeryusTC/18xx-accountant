import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Response, Http } from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { ColorsService } from './colors.service';

describe('ColorsService', () => {
	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [
				ColorsService,
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

	it('should ...', inject([ColorsService], (service: ColorsService) => {
		expect(service).toBeTruthy();
	}));
});
