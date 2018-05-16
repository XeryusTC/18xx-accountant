import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { Game }        from './models/game';
import { GameService } from './game.service';

describe('GameService', () => {
	let service: GameService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;
	let testGames: Game[] = [
		new Game('game-uuid-1', 12000),
		new Game('game-uuid-2', 9000)
	];

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions());
		service = new GameService(httpService);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('getGames() queries the correct url', () => {
		service.getGames();
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch(/game$/, 'url valid');
	});

	it('getGames() returns an array of games on success', done => {
		service.getGames().then(response => {
			expect(response).toEqual(testGames);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testGames)
		})));
	});

	it('getGames() should return an error when server is down', done => {
		service.getGames()
			.then(game => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('getGame() queries the correct url', () => {
		service.getGame('game-uuid');
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch(/game\/game-uuid$/, 'url valid');
	});

	it('getGame() returns a game on success', done => {
		service.getGame('game-uuid-1').then(response => {
			expect(response).toEqual(testGames[0]);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testGames[0])
		})));
	});

	it('getGame() should return an error when server is down', done => {
		service.getGame('test-uuid')
			.then(game => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('create() queries the correct url', () => {
		service.create(testGames[0]);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch(/game$/, 'url valid');
	});

	it('create() returns a game on success', done => {
		service.create(testGames[1]).then(response => {
			expect(response).toEqual(testGames[1]);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testGames[1])
		})));
	});

	it('create() should return an error when server is down', done => {
		service.create(testGames[0])
			.then(game => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
