import { TestBed, inject } from '@angular/core/testing';

import { Company }                 from './models/company';
import { Player }                  from './models/player';
import { SelectedInstanceService } from './selected-instance.service';

describe('SelectedInstanceService', () => {
	let service: SelectedInstanceService;
	let testCompany = new Company('company-uuid', 'game-uuid', 'B&O', 0, 10);
	let testPlayer = new Player('player-uuid', 'game-uuid', 'Alice', 1);

	beforeEach(() => {
		service = new SelectedInstanceService;
	});

	it('no player is selected after creation', () => {
		expect(service.selectedPlayer).toBeNull();
	});

	it('selectPlayer() should set to player UUID', () => {
		expect(service.selectedPlayer).toBeNull();
		service.selectPlayer(testPlayer);
		expect(service.selectedPlayer).toBe(testPlayer.uuid);
	});

	it('selectPlayer() should unset the selected company', () => {
		service.selectedCompany = testCompany.uuid;
		service.selectPlayer(testPlayer);
		expect(service.selectedCompany).toBeNull();
	});

	it('no company is selected after creation', () => {
		expect(service.selectedCompany).toBeNull();
	});

	it('selectCompany() should set to company UUID', () => {
		expect(service.selectedCompany).toBeNull();
		service.selectCompany(testCompany);
		expect(service.selectedCompany).toBe(testCompany.uuid);
	});

	it('selectCompany() should unset the selected player', () => {
		service.selectedPlayer = testPlayer.uuid;
		service.selectCompany(testCompany);
		expect(service.selectedPlayer).toBeNull();
	});
});
