import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { Player }        from './models/player';
import { PlayerService } from './player.service';

describe('PlayerService', () => {
	let service: PlayerService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testPlayer: Player = new Player('test-uuid', 'test-game', 'Alice',
										500);

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions);
		service = new PlayerService(httpService);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('getPlayer() queries the correct url', () => {
		service.getPlayer('some-uuid');
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('api/player/some-uuid/', 'url valid');
	});

	it('getPlayer() returns a player on success', done => {
		service.getPlayer('test-uuid').then(response => {
			expect(response).toEqual(testPlayer);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testPlayer)
		})));
	});

	it('getPlayer() should return an error when server is down', done => {
		service.getPlayer('test-uuid')
			.then(player => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('create() queries the correct url', () => {
		service.create(testPlayer);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('api/player/', 'url valid');
	});

	it('create() returns a player on success', done => {
		service.create(testPlayer).then(response => {
			expect(response).toEqual(testPlayer);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testPlayer)
		})));
	});

	it('create() should return an error when server is down', done => {
		service.create(testPlayer)
			.then(player => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
