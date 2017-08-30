import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';

import { Game } from '../models/game';
import { GameStateService } from '../game-state.service';
import { SettingsSectionComponent } from './settings-section.component';

describe('SettingsSectionComponent', () => {
	let component: SettingsSectionComponent;
	let fixture: ComponentFixture<SettingsSectionComponent>;

	let gameStateStub = {
		game: new Game('game-uuid', 12000, true)
	};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [ FormsModule ],
			declarations: [ SettingsSectionComponent ],
			providers: [
				{provide: GameStateService, useValue: gameStateStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(SettingsSectionComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
