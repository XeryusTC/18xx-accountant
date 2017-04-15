import { Player } from './player';

describe('Player model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'this can savely be ignored',
			uuid: 'fake-uuid',
			name: 'Alice',
			game: 'fake-game-uuid',
			cash: 700,
			shares: ['share-1-uuid', 'share-2-uuid']
		};
		let player = Player.fromJson(json);
		// Test each property individually instead of looping over them
		// because that will miss some properties
		expect(player.uuid).toEqual(json.uuid);
		expect(player.name).toEqual(json.name);
		expect(player.game).toEqual(json.game);
		expect(player.cash).toEqual(json.cash);
		expect(player.shares).toEqual(json.shares);
	});
});
