import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GameStateService }    from '../game-state.service';
import { LogSectionComponent } from './log-section.component';

describe('LogSectionComponent', () => {
	let component: LogSectionComponent;
	let fixture: ComponentFixture<LogSectionComponent>;
	let gameStateStub = {};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ LogSectionComponent ],
			providers: [
				{provide: GameStateService, useValue: gameStateStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(LogSectionComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});
});
