import { async, ComponentFixture, TestBed, fakeAsync, tick}
	from '@angular/core/testing';
import { FormsModule } from '@angular/forms';

import { Company }              from '../models/company';
import { Game }                 from '../models/game';
import { Player }               from '../models/player';
import { GameStateService }     from '../game-state.service';
import { OperateFormComponent } from './operate-form.component';
import { OperateService }       from '../operate.service';

describe('OperateFormComponent', () => {
	let component: OperateFormComponent;
	let fixture: ComponentFixture<OperateFormComponent>;
	let testCompany: Company;
	let gameStateStub;
	let operateServiceStub;

	beforeEach(async(() => {
		operateServiceStub = jasmine
			.createSpyObj('OperateService', ['operate']);
		operateServiceStub.operate.and.callFake(() => Promise.resolve(null));
		gameStateStub = jasmine
			.createSpyObj('GameStateService', ['updateGame', 'updatePlayer',
						  'updateCompany']);

		TestBed.configureTestingModule({
			imports: [FormsModule],
			declarations: [OperateFormComponent],
			providers: [
				{provide: GameStateService, useValue: gameStateStub},
				{provide: OperateService, useValue: operateServiceStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		testCompany = new Company('company-uuid', 'game-uuid', 'NNH', 0, 10);
		fixture = TestBed.createComponent(OperateFormComponent);
		component = fixture.componentInstance;
	});

	it('should create', () => {
		fixture.detectChanges();
		expect(component).toBeTruthy();
	});

	it('revenue is zero by default', () => {
		expect(component.revenue).toBe(0);
	});

	it('operate() uses correct amount of revenue', () => {
		component.revenue = 130;
		component.operate('full');
		expect(operateServiceStub.operate.calls.first().args[1]).toBe(130);
	});

	it('operate() uses correct company', () => {
		component.company = testCompany;
		component.operate('full');
		expect(operateServiceStub.operate.calls.first().args[0])
			.toBe(testCompany);
	});

	it('full() calls operate() with method set to full', () => {
		let operateSpy = spyOn(component, 'operate');
		component.full();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('full');
	});

	it('half() calls operate() with method set to half', () => {
		let operateSpy = spyOn(component, 'operate');
		component.half();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('half');
	});

	it('withhold() calls operate() with method set to withhold', () => {
		let operateSpy = spyOn(component, 'operate');
		component.withhold();
		expect(operateSpy.calls.any()).toBeTruthy();
		expect(operateSpy.calls.first().args[0]).toBe('withhold');
	});

	it('game instance should be updated when affected', fakeAsync(() => {
		let newGame = new Game('game-uuid', 1);
		operateServiceStub.operate
			.and.callFake(() => Promise.resolve({game: newGame}));
		component.operate('any');
		tick();
		expect(gameStateStub.updateGame.calls.first().args[0]).toBe(newGame);
	}));

	it('player instances should be updated when affected', fakeAsync(() => {
		let newPlayers = [new Player('player-uuid-0', 'game-uuid', 'Alice', 0),
			new Player('player-uuid-1', 'game-uuid', 'Alice', 1)];
		operateServiceStub.operate
			.and.callFake(() => Promise.resolve({players: newPlayers}));
		component.operate('any');
		tick();
		expect(gameStateStub.updatePlayer.calls.count()).toBe(2);
		expect(gameStateStub.updatePlayer.calls.argsFor(0)[0])
			.toBe(newPlayers[0]);
		expect(gameStateStub.updatePlayer.calls.argsFor(1)[0])
			.toBe(newPlayers[1]);
	}));

	it('company instances should be updated when affected', fakeAsync(() => {
		let newCompanies = [
			new Company('company-uuid-0', 'game-uuid', 'C&O', 0, 10),
			new Company('company-uuid-1', 'game-uuid', 'PRR', 0, 10),
			new Company('company-uuid-2', 'game-uuid', 'Erie', 0, 10)
		];
		operateServiceStub.operate
			.and.callFake(() => Promise.resolve({companies: newCompanies}));
		component.operate('any');
		tick();
		expect(gameStateStub.updateCompany.calls.count()).toBe(3);
		expect(gameStateStub.updateCompany.calls.argsFor(0)[0])
			.toBe(newCompanies[0]);
		expect(gameStateStub.updateCompany.calls.argsFor(1)[0])
			.toBe(newCompanies[1]);
		expect(gameStateStub.updateCompany.calls.argsFor(2)[0])
			.toBe(newCompanies[2]);
	}));
});
