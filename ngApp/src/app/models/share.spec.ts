import { Share } from './share';

describe('Share model', () => {
	it('fromJson should fill all fields', () => {
		let json= {
			url: 'thiscanbeignore',
			uuid: 'share-uuid',
			owner: 'player-uuid',
			company: 'company-uuid',
			shares: 3
		};
		let share = Share.fromJson(json);
		expect(share.uuid).toEqual(json.uuid);
		expect(share.owner).toEqual(json.owner);
		expect(share.company).toEqual(json.company);
		expect(share.shares).toEqual(json.shares);
	});
});
