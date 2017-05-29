import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By }                               from '@angular/platform-browser';
import { DebugElement }                     from '@angular/core';

import { ErrorDisplayComponent } from './error-display.component';
import { ErrorService }          from '../error.service';

describe('ErrorDisplayComponent', () => {
	let component: ErrorDisplayComponent;
	let fixture: ComponentFixture<ErrorDisplayComponent>;
	let errorService;
	let errors: DebugElement[];
	let close: DebugElement;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ ErrorDisplayComponent ],
			providers: [
				ErrorService
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(ErrorDisplayComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();

		errorService = fixture.debugElement.injector.get(ErrorService);
	});

	function updateElements(): void {
		fixture.detectChanges();
		errors = fixture.debugElement.queryAll(By.css('.error'));
		close = fixture.debugElement.query(By.css('.close'));
	}

	it('should create', () => {
		expect(component).toBeTruthy();
	});

	it('should not be visible when there are no errors', () => {
		updateElements();
		expect(errors).toEqual([]);
		expect(close).toBeNull();
	});

	it('displays errors in the service', () => {
		errorService.addError('Error 1');
		errorService.addError('Error 2');
		updateElements();
		expect(errors[0].nativeElement.innerHTML).toMatch('Error 1');
		expect(errors[1].nativeElement.innerHTML).toMatch('Error 2');
	});

	it('displays close button when there are errors', () => {
		errorService.addError('Error 0');
		updateElements();
		expect(close).toBeTruthy();
	});
});
