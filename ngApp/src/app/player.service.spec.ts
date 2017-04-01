import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http } from '@angular/http';
import {MockBackend } from '@angular/http/testing';

import { PlayerService } from './player.service';

describe('PlayerService', () => {
	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [
				PlayerService,
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

	it('should ...', inject([PlayerService], (service: PlayerService) => {
		expect(service).toBeTruthy();
	}));
});
