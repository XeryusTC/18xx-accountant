import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { AddPlayerComponent } from './add-player.component';

describe('AddPlayerComponent', () => {
	let component: AddPlayerComponent;
	let fixture: ComponentFixture<AddPlayerComponent>;
	let activatedRoute: ActivatedRouteStub;

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		TestBed.configureTestingModule({
			declarations: [AddPlayerComponent],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddPlayerComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
