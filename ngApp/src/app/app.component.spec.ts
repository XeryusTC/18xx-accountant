import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { By }                               from '@angular/platform-browser';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { RouterOutletStubComponent } from './testing/router-stubs';

import { AppComponent } from './app.component';

describe('AppComponent', () => {
	let fixture: ComponentFixture<AppComponent>;
	let comp: AppComponent;
	let el: HTMLElement;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [
				AppComponent,
				RouterOutletStubComponent
			],
			schemas: [NO_ERRORS_SCHEMA]
		}).compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AppComponent);
		comp = fixture.componentInstance;
	});

	it('should create the app', async(() => {
		expect(comp).toBeTruthy();
	}));

	it(`should have a router outlet`, async(() => {
		el = fixture.debugElement.query(By.css('router-outlet')).nativeElement;
		expect(el).toBeTruthy();
	}));

	it('should have the error display', () => {
		el = fixture.debugElement.query(By.css('error-display')).nativeElement;
		expect(el).toBeTruthy();
	});
});
