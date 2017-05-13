import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend }     from '@angular/http/testing';

import { Company }        from './models/company';
import { OperateService } from './operate.service';

describe('OperateService', () => {
	let service: OperateService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testCompany: Company;

	beforeEach(() => {
		backend = new MockBackend();
		backend.connections.subscribe(connection => conn = connection);
		httpService = new Http(backend, new BaseRequestOptions());
		service = new OperateService(httpService);
		testCompany = new Company('company-uuid', 'game-uuid', 'B&O', 0, 10);
	});

	it('operate() queries the correct url', () => {
		service.operate(testCompany, 10, 'full');
		expect(conn).toBeDefined('no http service at all');
		expect(conn.request.url).toMatch('/api/operate/$', 'url valid');
	});

	it('returns an error when server is down', done => {
		service.operate(testCompany, 10, 'full')
			.then(response => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
