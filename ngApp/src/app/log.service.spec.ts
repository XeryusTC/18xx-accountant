import { TestBed, inject } from '@angular/core/testing';
import { BaseRequestOptions, Http, Response, ResponseOptions }
	from '@angular/http';
import { MockBackend } from '@angular/http/testing';

import { LogEntry } from './models/log-entry';
import { LogService } from './log.service';

describe('LogService', () => {
	let service: LogService;
	let httpService: Http;
	let backend: MockBackend;
	let conn;

	let testLog: LogEntry[] = [
		new LogEntry('uuid-0', 'game-uuid', new Date('1970-01-01T00:00'),
					 'First entry'),
		new LogEntry('uuid-1', 'game-uuid', new Date('1970-01-02T00:00'),
					 '2nd entry'),
		new LogEntry('uuid-2', 'game-uuid', new Date('1970-01-03T00:00'),
					 'Third entry')
	];

	beforeEach(() => {
		backend = new MockBackend();
		httpService = new Http(backend, new BaseRequestOptions);
		service = new LogService(httpService);
		backend.connections.subscribe(connection => conn = connection);
	});

	it('getLog() queries the correct url', () => {
		service.getLog('game-uuid');
		expect(conn).toBeDefined('no http service connection at all?');
		expect(conn.request.url).toMatch(/logentry\?game=game-uuid$/,
										 'url invalid');
	});

	it('getLog() returns a complete log on success', done => {
		service.getLog('game-uuid').then(response => {
			expect(response).toEqual(testLog);
			done();
		});
		conn.mockRespond(new Response(new ResponseOptions({
			body: JSON.stringify(testLog)
		})));
	});

	it('getLog() should return an error when server is down', done => {
		service.getLog('game-uuid')
			.then(log => fail('The request should not be successful.'))
			.catch(error => done());
		conn.mockRespond(new Response(new ResponseOptions({
			status: 404,
			statusText: 'URL not found',
			body: 'The page could not be found'
		})));
	});
});
