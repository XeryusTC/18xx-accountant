import { async, ComponentFixture, TestBed, fakeAsync, tick }
	from '@angular/core/testing';
import { By }                               from '@angular/platform-browser';
import { FormsModule }                      from '@angular/forms';

import { Company }              from '../models/company';
import { Game }                 from '../models/game';
import { LogEntry }             from '../models/log-entry';
import { Player }               from '../models/player';
import { Share }                from '../models/share';
import { GameService }          from '../game.service';
import { GameStateService }     from '../game-state.service';
import { ShareFormComponent }   from './share-form.component';
import { TransferShareService } from '../transfer-share.service';
import { ValuesPipe }           from '../values.pipe';

describe('ShareFormComponent', () => {
	let component: ShareFormComponent;
	let fixture: ComponentFixture<ShareFormComponent>;
	let gameStateStub;
	let transferShareStub;

	let buyCompany = new Company('buy-uuid', 'game-uuid', 'RDR', 100, 10),
		shareCompany = new Company('share-uuid', 'game-uuid', 'PMQ', 0, 10),
		sourceCompany = new Company('source-uuid', 'game-uuid', 'NNH', 50, 10);
	let buyPlayer = new Player('buy-player', 'game-uuid', 'Alice', 200),
		sourcePlayer = new Player('source-player', 'game-uuid', 'Charlie', 10);

	function submitForm() {
		fixture.debugElement.query(By.css('form'))
			.triggerEventHandler('submit', new Event('submit'));
	}

	beforeEach(async(() => {
		gameStateStub = jasmine
			.createSpyObj('GameStateService', ['updateGame', 'updatePlayer',
						  'updateCompany', 'updateShare', 'companies',
						  'updateLog', 'ownsShare']);
		gameStateStub.players = {
			[buyPlayer.uuid]: buyPlayer,
			[sourcePlayer.uuid]: sourcePlayer
		};
		gameStateStub.companies = {
			[buyCompany.uuid]: buyCompany,
			[shareCompany.uuid]: shareCompany,
			[sourceCompany.uuid]: sourceCompany
		};

		transferShareStub = jasmine
			.createSpyObj('TransferShareService', ['transferShare']);
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve(null));

		TestBed.configureTestingModule({
			imports: [ FormsModule ],
			declarations: [ ShareFormComponent, ValuesPipe ],
			providers: [
				{provide: GameStateService, useValue: gameStateStub},
				{provide: TransferShareService, useValue: transferShareStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(ShareFormComponent);
		component = fixture.componentInstance;
		component.company_share = shareCompany.uuid;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('source is ipo by default', () => {
		expect(component.source).toBe('ipo');
	});

	it('amount of shares is one by default', () => {
		expect(component.share_amount).toBe(1);
	});

	it('action is buy by default', () => {
		expect(component.action).toBe('buy');
	});

	it('onSubmit() uses correct amount of shares', () => {
		component.share_amount = 42;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[4]).toBe(42);
	});

	it('onSubmit() allows the ipo to buy a share', () => {
		component.buyer = 'ipo';
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[0]).toBe('ipo');
	});

	it('onSubmit() allows the bank pool to buy a share', () => {
		component.buyer = 'bank';
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[0]).toBe('bank');
	});

	it('onSubmit() allows a company to buy a share', () => {
		component.buyer = buyCompany;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[0]).toBe(buyCompany);
	});

	it('onSubmit() allows a player to buy a share', () => {
		component.buyer = buyPlayer;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[0]).toBe(buyPlayer);
	});

	it('onSubmit() allows a share to be bought from the ipo', () => {
		component.source = 'ipo';
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[2]).toBe('ipo');
	});

	it('onSubmit() allows a share to be bought from the bank pool', () => {
		component.source = 'bank';
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[2]).toBe('bank');
	});

	it('onSubmit() allows a share to be bought from a company', () => {
		component.source = sourceCompany.uuid;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[2]).toBe(sourceCompany);
	});

	it('onSubmit() allows a share to be bought from a player', () => {
		component.source = sourcePlayer.uuid;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[2]).toBe(sourcePlayer);
	});

	it('onSubmit() correctly sets the company a share is bought in', () => {
		component.company_share = shareCompany.uuid;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[1]).toBe(shareCompany);
	});

	it('onSubmit() currectly sets the price of the share', () => {
		shareCompany.value = 82;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[3]).toBe(82);
	});

	it('onSubmit() uses negative shares when the action is sell', () => {
		shareCompany.value = 100;
		component.action = 'sell'
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[4]).toBe(-1);
	});

	it('game instance should be updated when affected', fakeAsync(() => {
		let newGame = new Game('game-uuid', 1);
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve({game: newGame}));
		submitForm();
		tick();
		expect(gameStateStub.updateGame.calls.first().args[0]).toBe(newGame);
	}));

	it('player instance should be updated when affected', fakeAsync(() => {
		let newPlayer = new Player('uuid', 'game-uuid', 'Alice', 7);
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve({players: [newPlayer]}));
		submitForm();
		tick();
		expect(gameStateStub.updatePlayer.calls.first().args[0])
			.toBe(newPlayer);
	}));

	it('company instance should be updated when affected', fakeAsync(() => {
		let newCompany = new Company('uuid', 'game-uuid', 'NNH', 2, 2);
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve({companies: [newCompany]}));
		submitForm();
		tick();
		expect(gameStateStub.updateCompany.calls.first().args[0])
			.toBe(newCompany);
	}));

	it('share instance should be updated when affected', fakeAsync(() => {
		let newShare = new Share('uuid', 'owner-uuid', 'comapny-uuid', 1);
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve({shares: [newShare]}));
		submitForm();
		tick();
		expect(gameStateStub.updateShare.calls.first().args[0])
			.toBe(newShare);
	}));

	it('adds error when given error response', fakeAsync(() => {
		transferShareStub.transferShare
			.and.callFake(() => Promise.reject({
				json: () => { return {non_field_errors:
					["This is a non-field error"]}
				}
			}));
		submitForm();
		tick();
		expect(component.errors).toEqual(['This is a non-field error']);
	}));

	it('log should be updated', fakeAsync(() => {
		let entry = new LogEntry('entry-uuid', 'game-uuid',
								 new Date(2017, 7, 23), 'test entry')
		transferShareStub.transferShare
			.and.callFake(() => Promise.resolve({log: entry}));
		submitForm();
		tick();
		expect(gameStateStub.updateLog.calls.first().args[0]).toBe(entry);
	}));
});
