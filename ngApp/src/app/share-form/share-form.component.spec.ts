import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By }                               from '@angular/platform-browser';
import { FormsModule }                      from '@angular/forms';

import { Company }              from '../models/company';
import { Player }               from '../models/player';
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
						  'updateCompany', 'companies']);
		gameStateStub.companies = {
			[buyCompany.uuid]: buyCompany,
			[shareCompany.uuid]: shareCompany,
			[sourceCompany.uuid]: sourceCompany
		};

		transferShareStub = jasmine
			.createSpyObj('TransferShareService', ['transferShare']);

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
		component.source = sourceCompany;
		submitForm();
		let args = transferShareStub.transferShare.calls.first().args;
		expect(args[2]).toBe(sourceCompany);
	});

	it('onSubmit() allows a share to be bought from a player', () => {
		component.source = sourcePlayer;
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
});
