import { TestBed, inject, fakeAsync, tick } from '@angular/core/testing';

import { Game }             from './models/game';
import { Player }           from './models/player';
import { Company }          from './models/company';

import { CompanyService }   from './company.service';
import { GameService }      from './game.service';
import { GameStateService, DIFFERENT_GAME_ERROR } from './game-state.service';
import { PlayerService }    from './player.service';

describe('GameStateService', () => {
	let service: GameStateService;
	let testGame = new Game('game-uuid', 12000);
	let testPlayers = [
		new Player('player-uuid-0', 'game-uuid', 'Alice', 100),
		new Player('player-uuid-1', 'game-uuid', 'Bob', 200),
		new Player('player-uuid-2', 'game-uuid', 'Charlie', 300)
	];
	let testCompanies = [
		new Company('company-uuid-0', 'game-uuid', 'B&O', 100, 10),
		new Company('company-uuid-1', 'game-uuid', 'PMQ', 200, 10),
		new Company('company-uuid-2', 'game-uuid', 'RDR', 300, 10)
	];

	// Game service mock
	let gameService    = jasmine.createSpyObj('gameService',
												 ['getGame', 'create']);
	gameService.getGame.and.callFake(() => Promise.resolve(testGame));

	// Player service mock
	let playerService  = jasmine.createSpyObj('playerService', ['getPlayer',
											  'getPlayerList', 'create']);
	playerService.getPlayerList
		.and.callFake(() => Promise.resolve(testPlayers));

	// Company service mock
	let companyService = jasmine.createSpyObj('companyService', ['getCompany',
											  'getCompanyList', 'create']);
	companyService.getCompanyList
		.and.callFake(() => Promise.resolve(testCompanies));

	beforeEach(() => {
		service = new GameStateService(gameService, playerService,
									   companyService);
	});

	it('loading a game use game service', () => {
		service.loadGame('test-game-uuid');
		expect(gameService.getGame.calls.first().args[0])
			.toBe('test-game-uuid');
	});

	it('loading a game sets the game instance', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.game).toEqual(testGame);
	}));

	it('loading a game retrieves players', () => {
		service.loadGame('game-uuid');
		expect(playerService.getPlayerList.calls.first().args[0])
			.toBe('game-uuid');
	});

	it('loading a game stores the players in a dictionary', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.players['player-uuid-0']).toEqual(testPlayers[0]);
		expect(service.players['player-uuid-1']).toEqual(testPlayers[1]);
		expect(service.players['player-uuid-2']).toEqual(testPlayers[2]);
	}));

	it('loading a game retrieves companies', () => {
		service.loadGame('game-uuid');
		expect(companyService.getCompanyList.calls.first().args[0])
			.toBe('game-uuid');
	});

	it('loading a game stores companies in a dictionary', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.companies['company-uuid-0']).toEqual(testCompanies[0]);
		expect(service.companies['company-uuid-1']).toEqual(testCompanies[1]);
		expect(service.companies['company-uuid-2']).toEqual(testCompanies[2]);
	}));

	it('updateGame() updates instance of game', fakeAsync(() => {
		let newGame = new Game('game-uuid', 11111);
		service.loadGame('game-uuid');
		tick();
		service.updateGame(newGame);
		expect(service.game).toEqual(newGame);
	}));

	it('cannot update game if UUIDs differ', fakeAsync(() => {
		let newGame = new Game('other-uuid', 3000);
		service.loadGame('game-uuid');
		tick();
		expect(() => service.updateGame(newGame))
			.toThrow(DIFFERENT_GAME_ERROR);
	}));

	it('updatePlayer() updates instance of player', fakeAsync(() => {
		let newPlayer = new Player('player-uuid-0', 'game-uuid', 'Dave', 5);
		service.loadGame('game-uuid');
		tick();
		service.updatePlayer(newPlayer);
		expect(service.players['player-uuid-0']).toEqual(newPlayer);
	}));

	it('updatePlayer() replaces list of players', fakeAsync(() => {
		let newPlayer = new Player('player-uuid-1', 'game-uuid', 'Eve', 17);
		service.loadGame('game-uuid');
		tick();
		let players = service.players;
		service.updatePlayer(newPlayer);
		expect(service.players).not.toBe(players);
	}));

	it('updateCompany() updates instance of company', fakeAsync(() => {
		let company = new Company('company-uuid-0', 'game-uuid', 'NNH', 10, 3);
		service.loadGame('game-uuid');
		tick();
		service.updateCompany(company);
		expect(service.companies['company-uuid-0']).toEqual(company);
	}));

	it('updateCompany() replaces list of companies', fakeAsync(() => {
		let company = new Company('company-uuid-1', 'game-uuid', 'B&M', 10, 7);
		service.loadGame('game-uuid');
		tick();
		let companies = service.companies;
		service.updateCompany(company);
		expect(service.companies).not.toBe(companies);
	}));
});
