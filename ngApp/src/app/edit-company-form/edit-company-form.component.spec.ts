import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';

import { ActivatedRoute, ActivatedRouteStub, Router }
	from '../testing/router-stubs';

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
	let routerSpy;

	let testColors = [['black', 'white'], ['red-50', 'red-100', 'red-200',
		'red-300', 'red-400', 'red-500', 'red-600', 'red-700', 'red-800',
		'red-900']];

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();

		colorsServiceStub = jasmine.createSpyObj('ColorsService',
												 ['getColors']);
		colorsServiceStub.getColors
			.and.callFake(() => Promise.resolve(testColors));

		companyServiceStub = jasmine.createSpyObj('CompanyService',
												  ['update']);
		companyServiceStub.update
			.and.callFake((company: Company) => Promise.resolve(company));

		gameStateStub = jasmine.createSpyObj('GameStateService',
											 ['companies']);
		gameStateStub.companies = {
			'test-company': new Company('test-company', 'game-uuid', 'Cie',
										0, 10),
			'other-company': new Company('other-company', 'game-uuid', 'B&O',
										 0, 10)
		};

		routerSpy = jasmine.createSpyObj('Router', ['navigate']);

		TestBed.configureTestingModule({
			imports: [ FormsModule ],
			declarations: [ EditCompanyFormComponent ],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				{provide: ColorsService, useValue: colorsServiceStub},
				{provide: CompanyService, useValue: companyServiceStub},
				{provide: GameStateService, useValue: gameStateStub},
				{provide: Router, useValue: routerSpy}
			]
		})
		.compileComponents();

		activatedRoute.testParams = {uuid: 'test-company'};
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
		activatedRoute.testParams = {uuid: 'other-company'};
		fixture.detectChanges();
		expect(component.model).toBe(gameStateStub.companies['other-company']);
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

	it('updates company on submit', fakeAsync(() => {
		fixture.detectChanges();
		component.onSubmit();
		tick();
		expect(companyServiceStub.update.calls.first().args[0])
			.toEqual(gameStateStub.companies['test-company']);
	}));

	it('navigates to the game on successful submit', fakeAsync(() => {
		fixture.detectChanges();
		component.onSubmit();
		tick();

		expect(routerSpy.navigate.calls.any())
			.toEqual(true, 'Router.navigate called');
		expect(routerSpy.navigate.calls.first().args[0])
			.toEqual(['game/', 'game-uuid']);
	}));

	it('displays non field errors on the page', fakeAsync(() => {
		let errors = {"non_field_errors": ["test error", "test_error_2"]};
		companyServiceStub.update
			.and.returnValue(Promise.reject({json: () => errors}));

		fixture.detectChanges();
		component.onSubmit();
		tick();

		expect(component.errors.length).toBe(2);
		expect(component.errors).toContain('test error');
		expect(component.errors).toContain('test_error_2');
	}));
});
