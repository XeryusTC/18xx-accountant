import { TestBed, inject, async, fakeAsync, tick }
	from '@angular/core/testing';
import { BaseRequestOptions, Response, Http, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { ColorsService } from './colors.service';

describe('ColorsService', () => {
	let service: ColorsService;
	let backend: MockBackend;
	let conn;
	let result;

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

		service = TestBed.get(ColorsService);
		backend = TestBed.get(MockBackend);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('should query the correct url', () => {
		service.getColors();
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('api/colors/', 'url valid');
	});

	it('should return an error when server is down', fakeAsync(() => {
		let catchedError;
		service.getColors()
			.then(colors => result = colors)
			.catch(error => catchedError = error);
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
		})));
		tick();
		expect(catchedError).toBeDefined();
		expect(result).toBeUndefined();
	}));

	it('should retrieve the list of colors', fakeAsync(() => {
		let response = JSON.stringify([
			['black', 'Black'],
			['white', 'White'],
			['red-500', 'Red 500']
		]);

		service.getColors().then(colors => result = colors);
		conn.mockRespond(new Response(new ResponseOptions({body: response})));
		tick();
		expect(result[0]).toContain('black');
		expect(result[0]).toContain('white',);
		expect(result[1]).toContain('red-500');
	}));

	it('should move the colors in a 10 wide grid', fakeAsync(() => {
		let response = JSON.stringify([['0-0', ''], ['0-1', ''], ['1-0', ''],
			 ['1-1', ''], ['1-2', ''], ['1-3', ''], ['1-4', ''], ['1-5', ''],
			 ['1-6', ''], ['1-7', ''], ['1-8', ''], ['1-9', ''], ['2-0', ''],
			 ['2-1', ''], ['2-2', ''], ['2-3', ''], ['2-4', ''], ['2-5', '']]);
		service.getColors().then(colors => result = colors);
		conn.mockRespond(new Response(new ResponseOptions({body: response})));
		tick();
		expect(result).toEqual([['0-0', '0-1'], ['1-0', '1-1', '1-2', '1-3',
			'1-4', '1-5', '1-6', '1-7', '1-8', '1-9'], ['2-0', '2-1', '2-2',
			'2-3', '2-4', '2-5']]);
	}));
});
