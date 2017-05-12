import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { CompanySectionComponent } from './company-section.component';
import { GameStateService }        from '../game-state.service';
import { SelectedInstanceService } from '../selected-instance.service';
import { ValuesPipe }              from '../values.pipe';

describe('CompanySectionComponent', () => {
	let component: CompanySectionComponent;
	let fixture: ComponentFixture<CompanySectionComponent>;
	let gameStateStub = {};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [CompanySectionComponent, ValuesPipe],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: GameStateService, useValue: gameStateStub},
				SelectedInstanceService
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(CompanySectionComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});
});
