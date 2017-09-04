import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { BaseRequestOptions, Http }         from '@angular/http';
import { MockBackend }                      from '@angular/http/testing';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';

import { Company }                  from '../models/company';
import { ColorsService }            from '../colors.service';
import { CompanyService }           from '../company.service';
import { GameStateService }         from '../game-state.service';
import { EditCompanyFormComponent } from './edit-company-form.component';

describe('EditCompanyFormComponent', () => {
	let component: EditCompanyFormComponent;
	let fixture: ComponentFixture<EditCompanyFormComponent>;
	// Services
	let activatedRoute: ActivatedRouteStub;
	let colorsServiceStub;
	let companyServiceStub;
	let gameStateStub;

	let testColors = [['black', 'white'], ['red-50', 'red-100', 'red-200',
		'red-300', 'red-400', 'red-500', 'red-600', 'red-700', 'red-800',
		'red-900']];

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		activatedRoute.testParams = {uuid: 'test'};
		colorsServiceStub = jasmine.createSpyObj('ColorsService',
												 ['getColors']);
		colorsServiceStub.getColors
			.and.callFake(() => Promise.resolve(testColors));

		gameStateStub = jasmine.createSpyObj('GameStateService',
											 ['companies']);
		gameStateStub.companies = {
			'test-company': new Company('test-company', 'game-uuid', 'Cie',
										0, 10)
		};

		TestBed.configureTestingModule({
			imports: [ FormsModule ],
			declarations: [ EditCompanyFormComponent ],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				{provide: ColorsService, useValue: colorsServiceStub},
				{provide: CompanyService, useValue: companyServiceStub},
				{provide: GameStateService, useValue: gameStateStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(EditCompanyFormComponent);
		component = fixture.componentInstance;

		let de = fixture.debugElement;
	});

	it('should be created', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('should get the company uuid from the current route', () => {
		activatedRoute.testParams = {uuid: 'test-company'};
		fixture.detectChanges();
		expect(component.model).toBe(gameStateStub.companies['test-company']);
	});

	it('Retrieve colors from ColorsService', () => {
		fixture.detectChanges();
		expect(colorsServiceStub.getColors.calls.any())
			.toBe(true, 'ColorsService.getColors() called');
	});

	it('take colors from ColorsService as-is', fakeAsync(() => {
		fixture.detectChanges();
		tick();
		expect(component.colors).toEqual(testColors);
	}));
});
