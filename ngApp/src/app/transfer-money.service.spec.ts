import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend }     from '@angular/http/testing';
import { Observable }      from 'rxjs/Observable';

import { Company }              from './models/company';
import { Player }               from './models/player';
import { TransferMoneyService } from './transfer-money.service';

describe('TransferMoneyService', () => {
	let service: TransferMoneyService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions());
		service = new TransferMoneyService(httpService);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('queries the correct url', () => {
		service.transferMoney(10, null, null);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('/api/transfer_money/$', 'url valid');
	});

	it('returns an error when server is down', done => {
		service.transferMoney(10, null, null)
			.then(response => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});

describe('TransferMoneyService request params', () => {
	let service: TransferMoneyService;
	let httpSpy;
	let testPlayer;
	let testCompany
	let call;

	beforeEach(() => {
		httpSpy = jasmine.createSpyObj('httpSpy', ['post']);
		httpSpy.post
			.and.callFake((url, data) => new Observable(observer => {
				observer.next(data);
				observer.complete();
			}));
		service = new TransferMoneyService(httpSpy);
		testPlayer = new Player('player-uuid', 'game-uuid', 'Alice', 100);
		testCompany = new Company('company-uuid', 'game-uuid', 'B&O', 10, 50);
	});

	it('recognizes when transfering from player', () => {
		service.transferMoney(10, testPlayer, null);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(10);
		expect(call.from_player).toBe(testPlayer.uuid);
		expect(call.from_company).toBeUndefined();
	});

	it('recognizes when transfering from company', () => {
		service.transferMoney(9, testCompany, null);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(9);
		expect(call.from_company).toBe(testCompany.uuid);
		expect(call.from_player).toBeUndefined();
	});

	it('recognizes when transfering to player', () => {
		service.transferMoney(8, null, testPlayer);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(8);
		expect(call.to_player).toBe(testPlayer.uuid);
		expect(call.to_company).toBeUndefined();
	});

	it('recognizes when transfering to company', () => {
		service.transferMoney(7, null, testCompany);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(7);
		expect(call.to_company).toBe(testCompany.uuid);
		expect(call.to_player).toBeUndefined();
	});

	it('transfer from bank by default', () => {
		service.transferMoney(6, null, null);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(6);
		expect(call.from_player).toBeUndefined();
		expect(call.from_company).toBeUndefined();
	});

	it('transfer to bank by default', () => {
		service.transferMoney(6, null, null);
		call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.amount).toBe(6);
		expect(call.to_player).toBeUndefined();
		expect(call.to_company).toBeUndefined();
	});
});
