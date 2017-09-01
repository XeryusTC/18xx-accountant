import { Game } from './game';

describe ('Game model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'thiscansavelybeignored',
			uuid: 'fake-uuid',
			players: ['player-1-uuid', 'player-2-uuid'],
			companies: ['company-1-uuid', 'company-2-uuid'],
			cash: 12000,
			pool_shares_pay: true,
			ipo_shares_pay: true,
			treasury_shares_pay: false
		};
		let game = Game.fromJson(json);
		// Test each property individually instead of looping over them
		// because that will miss some properties
		expect(game.uuid).toEqual(json.uuid);
		expect(game.cash).toEqual(json.cash);
		expect(game.players).toEqual(json.players);
		expect(game.companies).toEqual(json.companies);
		expect(game.pool_shares_pay).toEqual(json.pool_shares_pay);
		expect(game.ipo_shares_pay).toEqual(json.ipo_shares_pay);
		expect(game.treasury_shares_pay).toEqual(json.treasury_shares_pay);
	});
});
