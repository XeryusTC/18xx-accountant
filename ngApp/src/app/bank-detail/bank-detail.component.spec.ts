import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Game } from '../models/game';
import { BankDetailComponent } from './bank-detail.component';

describe('BankDetailComponent', () => {
	let component: BankDetailComponent;
	let fixture: ComponentFixture<BankDetailComponent>;
	let game: Game;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ BankDetailComponent ]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(BankDetailComponent);
		component = fixture.componentInstance;
		// Pretend that the component got a game as input
		game = new Game('uuid', 12000);
		component.game = game;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
