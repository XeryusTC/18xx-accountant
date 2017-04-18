import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By }                               from '@angular/platform-browser';

import { Game } from '../models/game';
import { BankDetailComponent } from './bank-detail.component';
import { GameStateService }    from '../game-state.service';

describe('BankDetailComponent', () => {
	let component: BankDetailComponent;
	let fixture: ComponentFixture<BankDetailComponent>;
	let elem;

	let gameStateStub = {
		game: new Game('game-uuid', 9000)
	};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ BankDetailComponent ],
			providers: [
				{provide: GameStateService, useValue: gameStateStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(BankDetailComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('shows current bank cash', () => {
		elem = fixture.debugElement.query(By.css('#cash')).nativeElement;
		expect(elem.textContent).toEqual('9000');
	});
});
