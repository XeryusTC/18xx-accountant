import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';

import { Company }              from '../models/company';
import { GameStateService }     from '../game-state.service';
import { OperateFormComponent } from './operate-form.component';
import { OperateService }       from '../operate.service';

describe('OperateFormComponent', () => {
	let component: OperateFormComponent;
	let fixture: ComponentFixture<OperateFormComponent>;
	let testCompany: Company;
	let gameStateStub;
	let operateServiceStub;

	beforeEach(async(() => {
		operateServiceStub = jasmine
			.createSpyObj('OperateService', ['operate']);
		gameStateStub = jasmine
			.createSpyObj('GameStateService', ['updateGame', 'updatePlayer',
						  'updateCompany']);
		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [OperateFormComponent],
			providers: [
				{provide: GameStateService, useValue: gameStateStub},
				{provide: OperateService, useValue: operateServiceStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		testCompany = new Company('company-uuid', 'game-uuid', 'NNH', 0, 10);
		fixture = TestBed.createComponent(OperateFormComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('revenue is zero by default', () => {
		expect(component.revenue).toBe(0);
	});

	it('operate() uses correct amount of revenue', () => {
		component.revenue = 130;
		component.operate('full');
		expect(operateServiceStub.operate.calls.first().args[1]).toBe(130);
	});

	it('operate() uses correct company', () => {
		component.company = testCompany;
		component.operate('full');
		expect(operateServiceStub.operate.calls.first().args[0])
			.toBe(testCompany);
	});

	it('full() calls operate() with method set to full', () => {
		let operateSpy = spyOn(component, 'operate');
		component.full();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('full');
	});

	it('half() calls operate() with method set to half', () => {
		let operateSpy = spyOn(component, 'operate');
		component.half();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('half');
	});

	it('withhold() calls operate() with method set to withhold', () => {
		let operateSpy = spyOn(component, 'operate');
		component.withhold();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('withhold');
	});
});
