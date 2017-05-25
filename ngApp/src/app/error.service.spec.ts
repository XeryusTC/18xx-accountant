import { TestBed, inject } from '@angular/core/testing';

import { ErrorService } from './error.service';

describe('ErrorService', () => {
	let service: ErrorService;

	beforeEach(() => {
		service = new ErrorService();
	});

	it('Should have no errors on creations', () => {
		expect(service.hasErrors()).toBe(false);
		expect(service.getErrors()).toEqual([]);
	});

	it('Can add error to list of errors', () => {
		service.addError('This is a test error');
		expect(service.hasErrors()).toBe(true);
		expect(service.getErrors()).toEqual(['This is a test error']);
	});

	it('Can remove all errors', () => {
		service.addError('Error 1');
		service.addError('Error 2');
		service.addError('Error 3');
		expect(service.hasErrors()).toBe(true);
		expect(service.getErrors()).toEqual(['Error 1', 'Error 2', 'Error 3']);
		service.clean();
		expect(service.hasErrors()).toBe(false);
		expect(service.getErrors()).toEqual([]);
	});
});
