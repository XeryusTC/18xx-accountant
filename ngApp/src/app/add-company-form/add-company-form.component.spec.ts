import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { BaseRequestOptions, Http }         from '@angular/http';
import { MockBackend }                      from '@angular/http/testing';

import { Router, RouterStub } from '../testing/router-stubs';

import { Company }                 from '../models/company';
import { AddCompanyFormComponent } from './add-company-form.component';
import { CompanyService }          from '../company.service';
import { ColorsService }           from '../colors.service';

describe('AddCompanyFormComponent', () => {
	let component: AddCompanyFormComponent;
	let fixture: ComponentFixture<AddCompanyFormComponent>;
	// Services
	let colorsService: ColorsService;
	let routerService: Router;
	let companyService: CompanyService;

	let testColors = [['black', 'white'], ['red-50', 'red-100', 'red-200',
		'red-300', 'red-400', 'red-500', 'red-600', 'red-700', 'red-800',
		'red-900']];
	let testCompany = new Company('test-uuid', 'test-game', 'B&O', 1000,
								  10, 'yellow-200', 'blue-600');

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [ AddCompanyFormComponent ],
			providers: [
				{
					provide: Http, useFactory: (backend, options) => {
						return new Http(backend, options);
					},
					deps: [MockBackend, BaseRequestOptions]
				},
				MockBackend,
				BaseRequestOptions,
				CompanyService,
				ColorsService,
				{provide: Router, useClass: RouterStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddCompanyFormComponent);
		component = fixture.componentInstance;

		let de = fixture.debugElement;
		colorsService  = de.injector.get(ColorsService);
		routerService  = de.injector.get(Router);
		companyService = de.injector.get(CompanyService);
	});

	it('Create', () => {
		expect(component).toBeTruthy();
	});

	it('Retrieve colors from ColorsService', () => {
		let spy = spyOn(colorsService, 'getColors')
			.and.returnValue(Promise.resolve(testColors));
		fixture.detectChanges();
		expect(spy.calls.any()).toBe(true, 'ColorsService.getColors() called');
	});

	it('Take colors from ColorService as-is', fakeAsync(() => {
		let spy = spyOn(colorsService, 'getColors')
			.and.returnValue(Promise.resolve(testColors));
		fixture.detectChanges();
		tick();
		expect(component.colors).toEqual(testColors);
	}));

	it('Create a new company on submit', fakeAsync(() => {
		let spy = spyOn(companyService, 'create')
			.and.returnValue(Promise.resolve(testCompany));
		component.model = testCompany;

		component.onSubmit();
		tick();
		expect(spy.calls.first().args[0]).toBe(testCompany);
	}));

	it('Navigate to the game on successful submit', fakeAsync(() => {
		let companyServiceSpy = spyOn(companyService, 'create')
			.and.returnValue(Promise.resolve(testCompany));
		let routerSpy = spyOn(routerService, 'navigate');
		component.model = testCompany;

		component.onSubmit();
		tick();

		expect(routerSpy.calls.any()).toBe(true, 'Router.navigate() called');
		expect(routerSpy.calls.first().args[0])
			.toEqual(['game/', 'test-game']);
	}));

	it('Display non field errors on the page', fakeAsync(() => {
		let errors = {"non_field_errors": ["test error", "test_error_2"]};
		let spy = spyOn(companyService, 'create')
			.and.returnValue(Promise.reject({json: () => errors}));

		component.onSubmit();
		tick();

		expect(component.errors.length).toBe(2);
		expect(component.errors).toContain('test error');
		expect(component.errors).toContain('test_error_2');
	}));
});
