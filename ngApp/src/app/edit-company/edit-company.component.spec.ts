import { NO_ERRORS_SCHEMA }                 from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Title, By }                        from '@angular/platform-browser';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { EditCompanyComponent } from './edit-company.component';

describe('EditCompanyComponent', () => {
	let component: EditCompanyComponent;
	let fixture: ComponentFixture<EditCompanyComponent>;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			schemas: [ NO_ERRORS_SCHEMA ],
			declarations: [ EditCompanyComponent ]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(EditCompanyComponent);
		component = fixture.componentInstance;
	});

	it('should be created', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('should set the page title to Edit company', () => {
		let titleService = fixture.debugElement.injector.get(Title);
		let spy = spyOn(titleService, 'setTitle');
		fixture.detectChanges();
		expect(spy.calls.any()).toBe(true);
		expect(spy.calls.first().args[0]).toBe('Edit company');
	});

	it('should include the menu', () => {
		let menu = fixture.debugElement.query(By.css('menu')).nativeElement;
		expect(menu).toBeTruthy();
	});
});
