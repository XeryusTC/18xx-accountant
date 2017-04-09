import { TestBed, inject, async } from '@angular/core/testing';
import { BaseRequestOptions, Response, Http, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { ColorsService } from './colors.service';

describe('ColorsService', () => {
	beforeEach(async() => {
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

	it('should retrieve the list of colors', done => {
		inject([ColorsService, MockBackend],
			(service: ColorsService, backend: MockBackend) => {
		let response = JSON.stringify([
			['black', 'Black'],
			['white', 'White'],
			['red-500', 'Red 500']
		]);
		backend.connections.subscribe(connection => {
			connection.mockRespond(new Response(new ResponseOptions(
				{body: response})));
		});

		service.getColors().then(colors => {
			expect(colors[0]).toContain('black');
			expect(colors[0]).toContain('white',);
			expect(colors[1]).toContain('red-500');
			done();
		});
	})() });

	it('should move the colors in a 10 wide grid', done => {
		inject([ColorsService, MockBackend],
			(service: ColorsService, backend: MockBackend) => {
			let response = JSON.stringify([['0-0', ''], ['0-1', ''],
				['1-0', ''], ['1-1', ''], ['1-2', ''], ['1-3', ''],
				['1-4', ''], ['1-5', ''], ['1-6', ''], ['1-7', ''],
				['1-8', ''], ['1-9', ''], ['2-0', ''], ['2-1', ''],
				['2-2', ''], ['2-3', ''], ['2-4', ''], ['2-5', '']]);
		backend.connections.subscribe(connection => {
			connection.mockRespond(new Response(new ResponseOptions(
				{body: response})));
		});

		service.getColors().then(colors => {
			console.log(colors);
			expect(colors).toEqual([['0-0', '0-1'], ['1-0', '1-1', '1-2', '1-3',
			'1-4', '1-5', '1-6', '1-7', '1-8', '1-9'], ['2-0', '2-1', '2-2',
			'2-3', '2-4', '2-5']]);
			done();
		});
	})() });
});
