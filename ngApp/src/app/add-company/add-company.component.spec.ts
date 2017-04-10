import { NO_ERRORS_SCHEMA }                 from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Title, By }                        from '@angular/platform-browser';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { AddCompanyComponent } from './add-company.component';

describe('AddCompanyComponent', () => {
	let component: AddCompanyComponent;
	let fixture: ComponentFixture<AddCompanyComponent>;
	let activatedRoute: ActivatedRouteStub;

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		TestBed.configureTestingModule({
			declarations: [AddCompanyComponent],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				Title
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddCompanyComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('should set the page title to Add company', () => {
		let titleService = fixture.debugElement.injector.get(Title);
		let spy = spyOn(titleService, 'setTitle');
		fixture.detectChanges();
		expect(spy.calls.any()).toBe(true);
	});

	it('should get the game uuid from the current rout', () => {
		expect(component.game_id).toBe(undefined);
		activatedRoute.testParams = {uuid: 'test uuid'};
		fixture.detectChanges();
		expect(component.game_id).toBe('test uuid');
	});

	it('should include the menu', () => {
		let menu = fixture.debugElement.query(By.css('menu')).nativeElement;
		expect(menu).toBeTruthy();
	});
});
