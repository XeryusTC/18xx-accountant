import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';
import { Observable }  from 'rxjs/Observable';

import { Company }              from './models/company';
import { Player }               from './models/player';
import { TransferShareService } from './transfer-share.service';

describe('TransferShareService', () => {
	let service: TransferShareService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testPlayer: Player;
	let testCompany: Company;

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions());
		service = new TransferShareService(httpService);
		backend.connections.subscribe(connection => conn = connection);
		testPlayer = new Player('player-uuid', 'game-uuid', 'Alice', 13);
		testCompany = new Company('company-uuid', 'game-uuid', 'NKP', 0, 10);
	});

	it('queries the correct url', () => {
		service.transferShare(testPlayer, testCompany, 'ipo', 17, 3);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/transfer_share/$', 'url valid');
	});

	it('returns an error when server is down', done => {
		service.transferShare(testPlayer, testCompany, 'ipo', 13, 2)
			.then(response => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});

describe('TransferShareService request params', () => {
	let service: TransferShareService,
		httpSpy,
		player: Player,
		sourcePlayer: Player,
		company: Company,
		sourceCompany: Company,
		call;

	beforeEach(() => {
		httpSpy = jasmine.createSpyObj('httpSpy', ['post']);
		httpSpy.post
			.and.callFake((url, data) => new Observable(observer => {
				observer.next(data);
				observer.complete();
			}));
		service = new TransferShareService(httpSpy);
		player = new Player('player-uuid', 'game-uuid', 'Alice', 1000);
		company = new Company('company-uuid', 'game-uuid', 'CPR', 700, 10);
		sourcePlayer = new Player('source-player-uuid', 'game-uuid', 'Bob',
								   900);
		sourceCompany = new Company('source-company-uuid', 'game-uuid',
									'Erie', 800, 10);
	});

	it('sets amount of shares to buy correctly', () => {
		service.transferShare(player, company, 'ipo', 0, 17);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(17);
	});

	it('sets share price correctly', () => {
		service.transferShare(player, company, 'ipo', 47, 1);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.price).toBe(47);
	});

	it('sets which share to buy correctly', () => {
		service.transferShare(player, company, 'ipo', 0, 0);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.share).toBe(company.uuid);
	});

	it('recognizes when buying from IPO', () => {
		service.transferShare(player, company, 'ipo', 1, 2);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.source_type).toBe('ipo');
		expect(call.company_source).toBeUndefined();
		expect(call.player_source).toBeUndefined();
	});

	it('recognizes when buying from bank', () => {
		service.transferShare(player, company, 'bank', 2, 3);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.source_type).toBe('bank');
		expect(call.company_source).toBeUndefined();
		expect(call.player_source).toBeUndefined();
	});

	it('recognizes when buying from company', () => {
		service.transferShare(player, company, sourceCompany, 3, 4);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.source_type).toBe('company');
		expect(call.company_source).toBe(sourceCompany.uuid);
		expect(call.player_source).toBeUndefined();
	});

	it('recognizes when buying from player', () => {
		service.transferShare(player, company, sourcePlayer, 4, 5);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.source_type).toBe('player');
		expect(call.company_source).toBeUndefined();
		expect(call.player_source).toBe(sourcePlayer.uuid);
	});

	it('recognizes when IPO is buyer', () => {
		service.transferShare('ipo', company, sourceCompany, 5, 6);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.buyer_type).toBe('ipo');
		expect(call.company_buyer).toBeUndefined();
		expect(call.player_buyer).toBeUndefined();
	});

	it('recognizes when bank is buyer', () => {
		service.transferShare('bank', company, sourceCompany, 6, 7);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.buyer_type).toBe('bank');
		expect(call.company_buyer).toBeUndefined();
		expect(call.player_buyer).toBeUndefined();
	});

	it('recognizes when player is buyer', () => {
		service.transferShare(player, company, sourceCompany, 7, 8);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.buyer_type).toBe('player');
		expect(call.company_buyer).toBeUndefined();
		expect(call.player_buyer).toBe(player.uuid);
	});

	it('recognizes when company is buyer', () => {
		service.transferShare(company, company, sourcePlayer, 5, 6);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.buyer_type).toBe('company');
		expect(call.company_buyer).toBe(company.uuid);
		expect(call.player_buyer).toBeUndefined();
	});
});
