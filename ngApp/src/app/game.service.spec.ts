import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http } from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { GameService } from './game.service';

describe('GameService', () => {
	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [
				GameService,
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

	it('should ...', inject([GameService], (service: GameService) => {
		expect(service).toBeTruthy();
	}));
});
