import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }              from '@angular/router/testing';

import { RouterLinkStubDirective } from '../testing/router-stubs';

import { Game }             from '../models/game';
import { MenuComponent }    from './menu.component';
import { NetWorthService }  from '../net-worth.service';
import { GameStateService } from '../game-state.service';

describe('MenuComponent', () => {
	let component: MenuComponent;
	let fixture: ComponentFixture<MenuComponent>;
	let gameServiceStub = {
		loadGame: (() => {}),
		game: new Game('test-game-uuid', 12000)
	};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [RouterTestingModule],
			declarations: [ MenuComponent, RouterLinkStubDirective ],
			providers: [
				{provide: GameStateService, useValue: gameServiceStub},
				NetWorthService
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(MenuComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
