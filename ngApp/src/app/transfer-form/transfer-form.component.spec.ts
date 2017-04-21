import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { By }          from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { Company }               from '../models/company';
import { Game }                  from '../models/game';
import { Player }                from '../models/player';
import { GameStateService }      from '../game-state.service';
import { TransferMoneyService }  from '../transfer-money.service';
import { TransferFormComponent } from './transfer-form.component';
import { ValuesPipe }            from '../values.pipe';

describe('TransferFormComponent', () => {
	let component: TransferFormComponent;
	let fixture: ComponentFixture<TransferFormComponent>;
	let transferMoneyStub;
	let gameStateStub;
	let company = new Company('some-uuid', 'game-uuid', 'B&O', 10, 57);
	let player = new Player('another-uuid', 'game-uuid', 'Alice', 83);

	function submitForm() {
		fixture.debugElement.query(By.css('form'))
			.triggerEventHandler('submit', new Event('submit'));
	}

	beforeEach(async(() => {
		transferMoneyStub = jasmine.createSpyObj('TransferMoneyService',
												 ['transferMoney']);
		transferMoneyStub.transferMoney
			.and.callFake(() => Promise.resolve({}));

		gameStateStub = jasmine
			.createSpyObj('GameStateService',
						  ['updateGame', 'updatePlayer', 'updateCompany',
						   'companies']);
		gameStateStub.companies = {[company.uuid]: company};
		gameStateStub.players   = {[player.uuid]:  player};

		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [ TransferFormComponent, ValuesPipe ],
			providers: [
				{provide: TransferMoneyService, useValue: transferMoneyStub},
				{provide: GameStateService, useValue: gameStateStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(TransferFormComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('amount is zero by default', () => {
		expect(component.amount).toBe(0);
	});

	it('target is bank by default', () => {
		expect(component.target).toBe('bank');
	});

	it('onSubmit() uses the correct amount of money', () => {
		component.amount = 1337;
		submitForm();
		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[0]).toBe(1337);
	});

	it('onSubmit() converts "bank" target to bank representation', () => {
		component.source = 'this is not it';
		submitForm();
		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[1]).toBe('this is not it');
		expect(args[2]).toBeNull();
	});

	it('onSubmit() recognises when transfering to company', () => {
		component.source = 'this is not it';
		component.target = company.uuid;
		submitForm();
		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[1]).toBe('this is not it');
		expect(args[2]).toBe(company);
	});

	it('onsubmit() recognises when transfering to player', () => {
		component.source = 'source-uuid';
		component.target = player.uuid;
		submitForm();
		let args = transferMoneyStub.transferMoney.calls.first().args;
		expect(args[1]).toBe('source-uuid');
		expect(args[2]).toBe(player);
	});

	it('game instance should be updated when it is affected', fakeAsync(() => {
		let newGame = new Game('game-uuid', 1);
		transferMoneyStub.transferMoney
			.and.callFake(() => Promise.resolve({game: newGame}));
		submitForm();
		tick();
		expect(gameStateStub.updateGame.calls.first().args[0]).toBe(newGame);
	}));

	it('player instance should be updated when it is affected',
	   fakeAsync(() => {
			let newPlayer = new Player('uuid', 'game-uuid', 'Alice', 7);
			transferMoneyStub.transferMoney
				.and.callFake(() => Promise.resolve({players: [newPlayer]}));
			submitForm();
			tick();
			expect(gameStateStub.updatePlayer.calls.first().args[0])
				.toBe(newPlayer)
	   }));

	it('company instance should be updated when affected', fakeAsync(() => {
		let newCompany = new Company('uuid', 'game-uuid', 'NYC', 10, 23);
		transferMoneyStub.transferMoney
			.and.callFake(() => Promise.resolve({companies: [newCompany]}));
		submitForm();
		tick();
		expect(gameStateStub.updateCompany.calls.first().args[0])
			.toBe(newCompany)
	}));
});
