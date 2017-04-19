import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { By }          from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { TransferMoneyService }  from '../transfer-money.service';
import { TransferFormComponent } from './transfer-form.component';

describe('TransferFormComponent', () => {
	let component: TransferFormComponent;
	let fixture: ComponentFixture<TransferFormComponent>;
	let transferMoneyStub;

	beforeEach(async(() => {
		transferMoneyStub = jasmine.createSpyObj('TransferMoneyService',
												 ['transferMoney']);
		transferMoneyStub.transferMoney
			.and.callFake(() => Promise.resolve(null));

		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [ TransferFormComponent ],
			providers: [
				{provide: TransferMoneyService, useValue: transferMoneyStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(TransferFormComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('amount is zero by default', () => {
		expect(component.amount).toBe(0);
	});

	it('target is bank by default', () => {
		expect(component.target).toBe('bank');
	});

	it('onSubmit() uses the correct amount of money', () => {
		component.amount = 1337;
		fixture.debugElement.query(By.css('form'))
			.triggerEventHandler('submit', new Event('submit'));
		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[0]).toBe(1337);
	});

	it('onSubmit() converts "bank" target to bank representation', () => {
		component.source = 'this is not it';
		fixture.debugElement.query(By.css('form'))
			.triggerEventHandler('submit', new Event('submit'));

		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[1]).toBe('this is not it');
		expect(args[2]).toBeNull();
	});
});
