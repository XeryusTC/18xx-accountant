import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { Router }                           from '@angular/router';

import { RouterStub } from '../testing/router-stubs';

import { Game }                   from '../models/game';
import { StartGameFormComponent } from './start-game-form.component';
import { GameService }            from '../game.service';

describe('StartGameFormComponent', () => {
	let component: StartGameFormComponent;
	let fixture: ComponentFixture<StartGameFormComponent>;
	let gameServiceStub = {
		create(game: Game) { }
	};
	let gameService;
	let gameServiceSpy;
	let testGame: Game = new Game('test-uuid', 12345);

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [ StartGameFormComponent ],
			providers: [
				{provide: GameService, useValue: gameServiceStub},
				{provide: Router,      useClass: RouterStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(StartGameFormComponent);
		component = fixture.componentInstance;
		gameService = fixture.debugElement.injector.get(GameService);
		gameServiceSpy = spyOn(gameService, 'create')
			.and.returnValue(Promise.resolve(testGame));
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});

	it('should create a game on submit', fakeAsync(() => {
		component.onSubmit();

		expect(gameServiceSpy.calls.any())
				.toBe(true, 'GameService.create() called');
	}));

	it('should navigate to the game on successful submit', fakeAsync(() => {
		let routerService = fixture.debugElement.injector.get(Router);
		let spy = spyOn(routerService, 'navigate')
		component.model = testGame;

		component.onSubmit();
		tick();

		expect(spy.calls.any()).toBe(true, 'Router.navigate() called');
		expect(spy.calls.first().args[0]).toEqual(['game/', 'test-uuid']);
	}));
});
