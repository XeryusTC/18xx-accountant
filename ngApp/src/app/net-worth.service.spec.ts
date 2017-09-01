import { TestBed, inject } from '@angular/core/testing';

import { NetWorthService } from './net-worth.service';

describe('NetWorthService', () => {
	let service: NetWorthService;

	beforeEach(() => {
		service = new NetWorthService;
	});

	it('net worth shouldnt be displayed by default', () => {
		expect(service.displayNetWorth).toBe(false);
	});

	it('toggleNetWorthDisplay() sets displayNetWorth when false', () => {
		service.displayNetWorth = false;
		service.toggleNetWorthDisplay();
		expect(service.displayNetWorth).toBe(true);
	});

	it('toggleNetWorthDisplay() unsets displayNetWorth when true', () => {
		service.displayNetWorth = true;
		service.toggleNetWorthDisplay();
		expect(service.displayNetWorth).toBe(false);
	});
});
