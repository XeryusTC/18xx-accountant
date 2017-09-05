import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';
import { Title }                            from '@angular/platform-browser';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { AddPlayerComponent } from './add-player.component';
import { GameStateService } from '../game-state.service';

describe('AddPlayerComponent', () => {
	let component: AddPlayerComponent;
	let fixture: ComponentFixture<AddPlayerComponent>;
	let activatedRoute: ActivatedRouteStub;
	let gameServiceStub;

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		activatedRoute.testParams = {uuid: 'test-game'};
		gameServiceStub = jasmine.createSpyObj('GameStateService',
											   ['loadGame', 'isLoaded']);
		TestBed.configureTestingModule({
			declarations: [AddPlayerComponent],
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
		fixture = TestBed.createComponent(AddPlayerComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
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
