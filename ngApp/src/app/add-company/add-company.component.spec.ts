import { NO_ERRORS_SCHEMA }                 from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Title, By }                        from '@angular/platform-browser';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { AddCompanyComponent } from './add-company.component';
import { GameStateService } from '../game-state.service';

describe('AddCompanyComponent', () => {
	let component: AddCompanyComponent;
	let fixture: ComponentFixture<AddCompanyComponent>;
	let activatedRoute: ActivatedRouteStub;
	let gameServiceStub;

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		activatedRoute.testParams = {uuid: 'test-game'};
		gameServiceStub = jasmine.createSpyObj('GameStateService',
											   ['isLoaded', 'loadGame']);

		TestBed.configureTestingModule({
			declarations: [AddCompanyComponent],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				{provide: GameStateService, useValue: gameServiceStub},
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

	it('should include the menu', () => {
		let menu = fixture.debugElement.query(By.css('menu')).nativeElement;
		expect(menu).toBeTruthy();
	});

	it('should not load a game if it is already loaded', () => {
		gameServiceStub.isLoaded.and.returnValue(true);
		fixture.detectChanges();
		expect(gameServiceStub.loadGame.calls.any()).toBe(false);
	});

	it('should load game if it is not already loaded', () => {
		gameServiceStub.isLoaded.and.returnValue(false);
		fixture.detectChanges();
		expect(gameServiceStub.loadGame.calls.any()).toBe(true);
		expect(gameServiceStub.loadGame.calls.first().args[0])
			.toBe('test-game');
	});
});
