import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';

import { Player }            from '../models/player';
import { Company }           from '../models/company';
import { GamePageComponent } from './game-page.component';
import { GameStateService } from '../game-state.service';
import { ValuesPipe } from '../values.pipe';

describe('GamePageComponent', () => {
	let component: GamePageComponent;
	let fixture: ComponentFixture<GamePageComponent>;
	let activatedRoute: ActivatedRouteStub;
	let gameStateSpy;

	let testPlayer  = new Player('test-uuid', 'game-uuid', 'Alice', 100);
	let testCompany = new Company('test-uuid', 'game-uuid', 'B&O', 200, 10);

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

	it('selectPlayer() should set a player', () => {
		expect(component.selectedPlayer).toBeUndefined();
		component.selectPlayer(testPlayer);
		expect(component.selectedPlayer).toBe(testPlayer);
	});

	it('selectPlayer() should unset the selectedCompany', () => {
		component.selectedCompany = testCompany;
		component.selectPlayer(testPlayer);
		expect(component.selectedCompany).toBeUndefined();
	});

	it('selectCompany() should set a company', () => {
		expect(component.selectedCompany).toBeUndefined();
		component.selectCompany(testCompany);
		expect(component.selectedCompany).toBe(testCompany);
	});

	it('selectCompany() should unset the selectedPlayer', () => {
		component.selectedPlayer = testPlayer;
		component.selectCompany(testCompany);
		expect(component.selectedPlayer).toBeUndefined();
	});
});
