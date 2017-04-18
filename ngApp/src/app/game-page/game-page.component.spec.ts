import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { GamePageComponent } from './game-page.component';
import { GameStateService } from '../game-state.service';
import { ValuesPipe } from '../values.pipe';

describe('GamePageComponent', () => {
	let component: GamePageComponent;
	let fixture: ComponentFixture<GamePageComponent>;
	let activatedRoute: ActivatedRouteStub;
	let gameStateSpy;

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		gameStateSpy = jasmine.createSpyObj('gameStateSpy', ['loadGame'])

		TestBed.configureTestingModule({
			declarations: [GamePageComponent, ValuesPipe],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				{provide: GameStateService, useValue: gameStateSpy}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		activatedRoute.testParams = {uuid: 'test'};
		fixture = TestBed.createComponent(GamePageComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('should get the game uuid from the current route', () => {
		expect(gameStateSpy.loadGame.calls.any()).toBeFalsy();
		activatedRoute.testParams = {uuid: 'test uuid'};
		fixture.detectChanges();
		expect(gameStateSpy.loadGame.calls.first().args[0]).toBe('test uuid');
	});
});
