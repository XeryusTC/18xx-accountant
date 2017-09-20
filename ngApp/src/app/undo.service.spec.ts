import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend }     from '@angular/http/testing';
import { Observable }      from 'rxjs/Observable';

import { Game }        from './models/game';
import { UndoService } from './undo.service';

describe('UndoService', () => {
	let service: UndoService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;

	let testGame = new Game('game-uuid', 1000);

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions);
		service = new UndoService(httpService);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('undo() queries the correct url', () => {
		service.undo(testGame);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('api/undo/', 'url valid');
	});

	it('undo() returns an error when server is down', done => {
		service.undo(testGame)
			.then(response => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});

	it('redo() queries the correct url', () => {
		service.redo(testGame);
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch('api/undo/', 'url valid');
	});

	it('redo() returns an error when server is down', done => {
		service.redo(testGame)
			.then(response => fail('The request should not be successful'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});

describe('UndoService request params', () => {
	let service: UndoService;
	let httpSpy;
	
	beforeEach(() => {
		httpSpy = jasmine.createSpyObj('httpSpy', ['post']);
		httpSpy.post
			.and.callFake((url, data) => new Observable(observer => {
				observer.next(data);
				observer.complete();
			}));
		service = new UndoService(httpSpy);
	});

	it('undo() adds correct parameters', () => {
		service.undo(new Game('game-uuid', 0));
		let call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.action).toBe('undo');
		expect(call.game).toBe('game-uuid');
	});

	it('redo() adds correct parameters', () => {
		service.redo(new Game('test-game-uuid', 0));
		let call = JSON.parse(httpSpy.post.calls.first().args[1]);
		expect(call.action).toBe('redo');
		expect(call.game).toBe('test-game-uuid');
	});
});
