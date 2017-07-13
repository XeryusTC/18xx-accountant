import { LogEntry } from './log-entry';

describe('LogEntry model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'this can be ignored',
			uuid: 'fake-uuid',
			game: 'fake-game-uuid',
			time: '1970-01-01T00:00:00.00000Z',
			text: 'lorem ipsum'
		};
		let logEntry = LogEntry.fromJson(json);

		expect(logEntry.uuid).toEqual(json.uuid);
		expect(logEntry.game).toEqual(json.game);
		expect(logEntry.time).toEqual(json.time);
		expect(logEntry.text).toEqual(json.text);
	});
});
