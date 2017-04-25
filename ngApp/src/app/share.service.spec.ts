import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend }     from '@angular/http/testing';

import { Share }        from './models/share';
import { ShareService } from './share.service';

describe('ShareService', () => {
	let service: ShareService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testShare: Share = new Share('test-uuid', 'test-player',
									 'test-company', 5);

	let testShareList: Share[] = [
		new Share('uuid-0', 'player-0', 'company-0', 2),
		new Share('uuid-1', 'player-0', 'company-1', 3),
		new Share('uuid-2', 'player-1', 'company-0', 5)
	];

	beforeEach(() => {
		backend = new MockBackend();
		backend.connections.subscribe(connection => conn = connection);
		httpService = new Http(backend, new BaseRequestOptions());
		service = new ShareService(httpService);
	});

	it('getPlayerShareList() queries the correct url for game', () => {
		service.getPlayerShareList('game-uuid');
		expect(conn).toBeDefined('no http service at all');
		expect(conn.request.url).toMatch('/api/playershare/\\?game=game-uuid$',
										 'url valid');
	});

	it('getPlayerShareList() queries the correct url for player', () => {
		service.getPlayerShareList('player-uuid', 'player');
		expect(conn).toBeDefined('no http service at all');
		expect(conn.request.url)
			.toMatch('/api/playershare/\\?player=player-uuid$', 'url valid');
	});


	it('getPlayerShareList() returns an error when server is down', done => {
		service.getPlayerShareList('game-uuid')
			.then(player => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('getCompanyShareList() queries the correct url for game', () => {
		service.getCompanyShareList('game-uuid');
		expect(conn).toBeDefined('no http service at all');
		expect(conn.request.url)
			.toMatch('/api/companyshare/\\?game=game-uuid$', 'url valid');
	});

	it('getCompanyShareList() queries the correct url for company', () => {
		service.getCompanyShareList('company-uuid', 'company');
		expect(conn).toBeDefined('no http service at all');
		expect(conn.request.url)
			.toMatch('/api/companyshare/\\?company=company-uuid$',
					 'url valid');
	});

	it('getCompanyShareList() returns an error when server is down', done => {
		service.getCompanyShareList('game-uuid')
			.then(player => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
