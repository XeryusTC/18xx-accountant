import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { Player }                 from '../models/player';
import { GameStateService }       from '../game-state.service';
import { PlayerSectionComponent } from './player-section.component';
import { ValuesPipe }             from '../values.pipe';
import { SelectedInstanceService } from '../selected-instance.service';

describe('PlayerSectionComponent', () => {
	let component: PlayerSectionComponent;
	let fixture: ComponentFixture<PlayerSectionComponent>;
	let gameStateStub = {};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [PlayerSectionComponent, ValuesPipe],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: GameStateService, useValue: gameStateStub},
				SelectedInstanceService
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(PlayerSectionComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
