import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { BaseRequestOptions, Http }         from '@angular/http';
import { MockBackend }                      from '@angular/http/testing';

import { Router, RouterStub } from '../testing/router-stubs';

import { Game }                   from '../models/game';
import { Player }                 from '../models/player';
import { AddPlayerFormComponent } from './add-player-form.component';
import { PlayerService }          from '../player.service';
import { GameStateService }       from '../game-state.service';

describe('AddPlayerFormComponent', () => {
	let component: AddPlayerFormComponent;
	let fixture: ComponentFixture<AddPlayerFormComponent>;
	let testPlayer: Player = new Player('test-uuid', 'test-game', 'Alice', 0);
	let playerService: PlayerService;
	let routerService: Router;
	let gameStateStub = {
		game: new Game('test-game', 12000)
	}

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [ FormsModule ],
			declarations: [ AddPlayerFormComponent ],
			providers: [
				PlayerService,
				{provide: GameStateService, useValue: gameStateStub},
				{provide: Router, useClass: RouterStub},
				{
					provide: Http, useFactory: (backend, options) => {
						return new Http(backend, options);
					},
					deps: [MockBackend, BaseRequestOptions]
				},
				MockBackend,
				BaseRequestOptions
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddPlayerFormComponent);
		component = fixture.componentInstance;

		let de = fixture.debugElement;
		playerService = de.injector.get(PlayerService);
		routerService = de.injector.get(Router);
	});

	it('Created', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('Create new player on submit', fakeAsync(() => {
		let spy = spyOn(playerService, 'create')
			.and.returnValue(Promise.resolve(testPlayer));
		component.model = testPlayer;

		component.onSubmit();
		tick();
		expect(spy.calls.first().args[0]).toBe(testPlayer);
	}));

	it('Navigates to the game on successful submit', fakeAsync(() => {
		let playerServiceSpy = spyOn(playerService, 'create')
			.and.returnValue(Promise.resolve(testPlayer));
		let routerSpy = spyOn(routerService, 'navigate');
		component.model = testPlayer;

		component.onSubmit();
		tick();

		expect(routerSpy.calls.any()).toBe(true, 'Router.navigate called');
		expect(routerSpy.calls.first().args[0])
			.toEqual(['game/', 'test-game']);
	}));

	it('Display non field errors on the page', fakeAsync(() => {
		let errors = {"non_field_errors": ["test error", "2nd error"]};
		let spy = spyOn(playerService, 'create')
			.and.returnValue(Promise.reject({json: () => errors}));

		component.onSubmit();
		tick();

		expect(component.errors.length).toBe(2);
		expect(component.errors).toContain("test error");
		expect(component.errors).toContain("2nd error");
	}));
});
