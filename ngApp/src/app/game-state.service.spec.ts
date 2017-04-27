import { TestBed, inject, fakeAsync, tick } from '@angular/core/testing';

import { Game }             from './models/game';
import { Player }           from './models/player';
import { Company }          from './models/company';
import { Share }            from './models/share';

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
	let testPlayerShares = [
		new Share('share-uuid-0', 'player-uuid-0', 'company-uuid-0', 2),
		new Share('share-uuid-1', 'player-uuid-0', 'company-uuid-1', 3),
		new Share('share-uuid-2', 'player-uuid-1', 'company-uuid-0', 5),
	];
	let testCompanyShares= [
		new Share('share-uuid-3', 'company-uuid-0', 'company-uuid-0', 2),
		new Share('share-uuid-4', 'company-uuid-1', 'company-uuid-1', 1),
		new Share('share-uuid-5', 'company-uuid-2', 'company-uuid-2', 3)
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

	// Share service mock
	let shareService = jasmine
		.createSpyObj('ShareService', ['getPlayerShareList',
					  'getCompanyShareList']);
	shareService.getPlayerShareList
		.and.callFake(() => Promise.resolve(testPlayerShares));
	shareService.getCompanyShareList
		.and.callFake(() => Promise.resolve(testCompanyShares));

	beforeEach(() => {
		service = new GameStateService(gameService, playerService,
									   companyService, shareService);
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

	it('loading a game retrieves shares', () => {
		service.loadGame('game-uuid');
		expect(shareService.getPlayerShareList.calls.first().args[0])
			.toBe('game-uuid');
		expect(shareService.getPlayerShareList.calls.first().args[0])
			.toBe('game-uuid');
	});

	it('loading a game stores shares in a single dictionary', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.shares['share-uuid-0']).toEqual(testPlayerShares[0]);
		expect(service.shares['share-uuid-1']).toEqual(testPlayerShares[1]);
		expect(service.shares['share-uuid-2']).toEqual(testPlayerShares[2]);
		expect(service.shares['share-uuid-3']).toEqual(testCompanyShares[0]);
		expect(service.shares['share-uuid-4']).toEqual(testCompanyShares[1]);
		expect(service.shares['share-uuid-5']).toEqual(testCompanyShares[2]);
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
		expect(service.players.length).toBe(players.length);
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
		expect(service.companies.length).toEqual(companies.length);
		console.log(service.companies.length, companies.length);
	}));

	it('updateShare() updates instance of share', fakeAsync(() => {
		let share = new Share('share-uuid-0', 'player-uuid-0',
							  'company-uuid-0', 7);
		service.loadGame('game-uuid');
		tick();
		service.updateShare(share);
		expect(service.shares['share-uuid-0']).toEqual(share);
	}));

	it('updateShare() replaces list of shares', fakeAsync(() => {
		let share = new Share('share-uuid-0', 'player-uuid-0',
							  'company-uuid-0', 9);
		service.loadGame('game-uuid');
		tick();
		let shares = service.shares;
		service.updateShare(share);
		expect(service.shares).not.toBe(shares);
		expect(service.shares.length).toEqual(shares.length);
	}));

	it('shareInfo() gives info on share holdings of player', fakeAsync(() => {
		testCompanies[0].text_color = 'color1';
		testCompanies[0].background_color = 'color2';
		testCompanies[1].text_color = 'color3';
		testCompanies[1].background_color = 'color4';
		testPlayers[0].share_set = ['share-uuid-0', 'share-uuid-1'];
		service.loadGame('game-uuid');
		tick();
		tick();
		let info = service.shareInfo(testPlayers[0]);
		expect(info[0]).toEqual({
			fraction: 0.2,
			shares: 2,
			share_count: 10,
			name: 'B&O',
			text_color: 'color1',
			background_color: 'color2'
		});
		expect(info[1]).toEqual({
			fraction: 0.3,
			shares: 3,
			share_count: 10,
			name: 'PMQ',
			text_color: 'color3',
			background_color: 'color4'
		});
	}));

	it('is not loaded after initial creation', () => {
		expect(service.isLoaded()).toBe(false);
	});

	it('marks as being loaded after loading game finishes', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.isLoaded()).toBe(true);
	}));

	it('calling loadGame() marks as being not loaded', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.isLoaded()).toBe(true);
		service.loadGame('game-uuid');
		expect(service.isLoaded()).toBe(false);
	}));
});
