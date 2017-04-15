import { Game } from './game';

describe ('Game model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'thiscansavelybeignored',
			uuid: 'fake-uuid',
			players: ['player-1-uuid', 'player-2-uuid'],
			companies: ['company-1-uuid', 'company-2-uuid'],
			cash: 12000
		};
		let game = Game.fromJson(json);
		// Test each property individually instead of looping over them
		// because that will miss some properties
		expect(game.uuid).toEqual(json.uuid);
		expect(game.game).toEqual(json.game);
		expect(game.players).toEqual(json.players);
		expect(game.companies).toEqual(json.companies);
	});
});
