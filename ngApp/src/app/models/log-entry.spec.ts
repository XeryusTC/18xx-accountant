import { LogEntry } from './log-entry';

describe('LogEntry model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'this can be ignored',
			uuid: 'fake-uuid',
			game: 'fake-game-uuid',
			time: '1970-01-02T03:04:05',
			text: 'lorem ipsum',
			acting_company: 'company-uuid',
			is_undoable: false
		};
		let logEntry = LogEntry.fromJson(json);

		expect(logEntry.uuid).toEqual(json.uuid);
		expect(logEntry.game).toEqual(json.game);
		expect(logEntry.time).toEqual(new Date(1970, 0, 2, 3, 4, 5, 0));
		expect(logEntry.text).toEqual(json.text);
		expect(logEntry.acting_company).toEqual(json.acting_company);
		expect(logEntry.is_undoable).toEqual(json.is_undoable);
	});
});
