import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GameStateService }  from '../game-state.service';
import { NetWorthComponent } from './net-worth.component';
import { NetWorthService }   from '../net-worth.service';
import { ValuesPipe }        from '../values.pipe';

describe('NetWorthComponent', () => {
	let component: NetWorthComponent;
	let fixture: ComponentFixture<NetWorthComponent>;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [NetWorthComponent, ValuesPipe],
			providers: [
				NetWorthService,
				{provide: GameStateService, useValue: {}}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(NetWorthComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
