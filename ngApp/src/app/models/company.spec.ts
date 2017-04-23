import { Company } from './company';

describe('Company model', () => {
	it('fromJson should fill all fields', () => {
		let json = {
			url: 'thiscansavelybeignored',
			uuid: 'fake-uuid',
			name: 'B&O',
			text_color: 'black',
			background_color: 'white',
			game: 'fake-game-uuid',
			cash: 100,
			share_count: 20,
			ipo_shares: 5,
			bank_shares: 4,
			player_owners: []
		};
		let company = Company.fromJson(json);
		// Test each property individually instead of looping over them
		// because that will miss some properties
		expect(company.uuid).toEqual(json.uuid);
		expect(company.name).toEqual(json.name);
		expect(company.game).toEqual(json.game);
		expect(company.cash).toEqual(json.cash);
		expect(company.share_count).toEqual(json.share_count);
		expect(company.text_color).toEqual(json.text_color);
		expect(company.background_color).toEqual(json.background_color);
		expect(company.bank_shares).toEqual(json.bank_shares);
		expect(company.ipo_shares).toEqual(json.ipo_shares);
		// Value should be 0 (this is not stored on the server)
		expect(company.value).toEqual(0);
	});
});
