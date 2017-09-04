import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { Company }        from './models/company';
import { CompanyService } from './company.service';

describe('CompanyService', () => {
	let service: CompanyService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testCompany: Company;
	let testCompanyList = [
		new Company('test-uuid-0', 'test-game', 'CP', 100, 10),
		new Company('test-uuid-1', 'test-game', 'PRR', 200, 10),
		new Company('test-uuid-2', 'test-game', 'Erie', 300, 10)
	];

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions);
		backend.connections.subscribe(connection => conn = connection);
		service = new CompanyService(httpService);
		testCompany = new Company('test-uuid', 'test-game', 'NYC', 500, 10);
		testCompany.bank_shares = 0;
		testCompany.ipo_shares = 0;
	});

	it('getCompany() queries the correct url', () => {
		service.getCompany('test-uuid');
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/company/test-uuid/$',
										 'url valid');
	});

	it('getCompany() returns a company on success', done => {
		service.getCompany('test-uuid').then(response => {
			expect(response).toEqual(testCompany);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testCompany)
		})));
	});

	it('getCompany() should return an error when server is dowwn', done => {
		service.getCompany('test-uuid')
			.then(company => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('getCompanyList() queries the correct url', () => {
		service.getCompanyList('game-uuid');
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/company/\\?game=game-uuid$',
										 'url valid');
	});

	it('getCompanyList() returns an array of companies on success', done => {
		service.getCompanyList('game-uuid').then(response => {
			expect(response).toEqual(testCompanyList);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testCompanyList)
		})));
	});

	it('getCompanyList() should return an error when server is down', done => {
		service.getCompanyList('game-uuid')
			.then(companies => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('create() queries the correct url', () => {
		service.create(testCompany);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/company/$', 'url valid');
	});

	it('create() returns a company on success', done => {
	   service.create(testCompany).then(response => {
		   expect(response).toEqual(testCompany);
		   done();
	   });
	   conn.mockRespond(new Response(new ResponseOptions({
		   body: JSON.stringify(testCompany)
	   })));
	});

	it('create() should return an error when server is down', done => {
		service.create(testCompany)
			.then(company => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('update() queries the correct url', () => {
		service.update(testCompany);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/company/test-uuid/$',
										 'url valid');
	});

	it('update() returns the updated company on success', done => {
		service.update(testCompany).then(response => {
			expect(response).toEqual(testCompany);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testCompany)
		})));
	});

	it('update() should return an error when server is down', done => {
		service.update(testCompany)
			.then(company => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
