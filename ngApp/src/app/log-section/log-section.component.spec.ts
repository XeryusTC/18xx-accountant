import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LogEntry }            from '../models/log-entry';
import { GameStateService }    from '../game-state.service';
import { LogSectionComponent } from './log-section.component';

describe('LogSectionComponent', () => {
	let component: LogSectionComponent;
	let fixture: ComponentFixture<LogSectionComponent>;
	let gameStateStub = {
		companies: {
			'company-uuid': {text_color: 'red-50', background_color: 'red-900'}
		}
	};

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

	it('entryColorClass should use company colors', () => {
		let entry = new LogEntry('entry-uuid', 'game-uuid',
								 new Date(2017, 7, 30), 'test entry',
								 'company-uuid');
		expect(component.entryColorClass(entry)).toBe('fg-red-50 bg-red-900');
	});

	it('entryColorClass should not include colors when no acting company',
	   () => {
		let entry = new LogEntry('entry-uuid', 'game-uuid',
								 new Date(2017, 7, 30), 'test entry', null);
		expect(component.entryColorClass(entry)).toBe('');
	});
});
