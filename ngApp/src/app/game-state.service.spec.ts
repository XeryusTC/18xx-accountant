import { TestBed, inject, fakeAsync, tick } from '@angular/core/testing';

import { Game }             from './models/game';
import { Player }           from './models/player';
import { Company }          from './models/company';
import { Share }            from './models/share';
import { LogEntry }         from './models/log-entry';

import { CompanyService }   from './company.service';
import { ErrorService }     from './error.service';
import { GameService }      from './game.service';
import { GameStateService, DIFFERENT_GAME_ERROR } from './game-state.service';
import { LogService }       from './log.service';
import { PlayerService }    from './player.service';
import { UndoService }      from './undo.service';

describe('GameStateService', () => {
	let service: GameStateService;

	// Data
	let testGame: Game;
	let testPlayers: Player[];
	let testCompanies: Company[];
	let testPlayerShares: Share[];
	let testCompanyShares: Share[];
	let testLog: LogEntry[];

	// Service mocks
	let gameService;
	let playerService;
	let companyService;
	let shareService;
	let errorService;
	let logService;
	let undoService;

	beforeEach(() => {
		testGame = new Game('game-uuid', 12000);
		testPlayers = [
			new Player('player-uuid-0', 'game-uuid', 'Alice', 100),
			new Player('player-uuid-1', 'game-uuid', 'Bob', 200),
			new Player('player-uuid-2', 'game-uuid', 'Charlie', 300)
		];
		testPlayers[0].share_set = [
			'share-uuid-0',
			'share-uuid-1',
			'share-uuid-6'
		];
		testCompanies = [
			new Company('company-uuid-0', 'game-uuid', 'B&O', 100, 10),
			new Company('company-uuid-1', 'game-uuid', 'PMQ', 200, 10),
			new Company('company-uuid-2', 'game-uuid', 'RDR', 300, 10),
			new Company('company-uuid-3', 'game-uuid', 'C&O', 400, 5)
		];
		testCompanies[0].share_set = ['share-uuid-3'];
		testPlayerShares = [
			new Share('share-uuid-0', 'player-uuid-0', 'company-uuid-1', 3),
			new Share('share-uuid-1', 'player-uuid-0', 'company-uuid-0', 2),
			new Share('share-uuid-2', 'player-uuid-1', 'company-uuid-0', 5),
			new Share('share-uuid-6', 'player-uuid-0', 'company-uuid-3', 2),
		];
		testCompanyShares = [
			new Share('share-uuid-3', 'company-uuid-0', 'company-uuid-0', 2),
			new Share('share-uuid-4', 'company-uuid-1', 'company-uuid-1', 1),
			new Share('share-uuid-5', 'company-uuid-2', 'company-uuid-2', 3)
		];
		testLog = [
			new LogEntry('log-uuid-0', 'game-uuid',
						 new Date('1970-01-01T01:01:01.0001Z'),
						 'First log entry'),
			new LogEntry('log-uuid-1', 'game-uuid',
						 new Date('1971-02-02T02:02:02.0002Z'),
						 'Second entry'),
			new LogEntry('log-uuid-2', 'game-uuid',
						 new Date('1972-03-03T03:03:03.0003Z'),
						 'Third log entry'),
		];


		// Game service mock
		gameService = jasmine.createSpyObj('gameService',
										   ['getGame', 'create']);
		gameService.getGame.and.callFake(() => Promise.resolve(testGame));

		// Player service mock
		playerService = jasmine.createSpyObj('playerService', ['getPlayer',
											 'getPlayerList', 'create']);
		playerService.getPlayerList
			.and.callFake(() => Promise.resolve(testPlayers));

		// Company service mock
		companyService = jasmine.createSpyObj('companyService',
											  ['getCompany',
											  'getCompanyList', 'create']);
		companyService.getCompanyList
			.and.callFake(() => Promise.resolve(testCompanies));

		// Share service mock
		shareService = jasmine.createSpyObj('ShareService',
											['getPlayerShareList',
											'getCompanyShareList']);

		shareService.getPlayerShareList
			.and.callFake(() => Promise.resolve(testPlayerShares));
		shareService.getCompanyShareList
			.and.callFake(() => Promise.resolve(testCompanyShares));

		// Error service mock
		errorService = jasmine.createSpyObj('ErrorService', ['getErrors',
											'hasErrors', 'addError']);

		// Log service mock
		logService = jasmine.createSpyObj('LogService', ['getLog']);
		logService.getLog
			.and.callFake(() => Promise.resolve(testLog));

		// Undo service mock
		undoService = jasmine.createSpyObj('UndoService', ['undo', 'redo']);
		undoService.undo.and.callFake(() => Promise.resolve({}));

		service = new GameStateService(gameService, playerService,
									   companyService, shareService,
									   errorService, logService, undoService);
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

	it('loading a game retrieves players', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(playerService.getPlayerList.calls.first().args[0])
			.toBe('game-uuid');
	}));

	it('loading a game stores the players in a dictionary', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.players['player-uuid-0']).toEqual(testPlayers[0]);
		expect(service.players['player-uuid-1']).toEqual(testPlayers[1]);
		expect(service.players['player-uuid-2']).toEqual(testPlayers[2]);
	}));

	it('loading a game retrieves companies', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(companyService.getCompanyList.calls.first().args[0])
			.toBe('game-uuid');
	}));

	it('loading a game stores companies in a dictionary', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.companies['company-uuid-0']).toEqual(testCompanies[0]);
		expect(service.companies['company-uuid-1']).toEqual(testCompanies[1]);
		expect(service.companies['company-uuid-2']).toEqual(testCompanies[2]);
	}));

	it('loading a game retrieves shares', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(shareService.getPlayerShareList.calls.first().args[0])
			.toBe('game-uuid');
		expect(shareService.getCompanyShareList.calls.first().args[0])
			.toBe('game-uuid');
	}));

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

	it('loading a game retrieves the log', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(logService.getLog.calls.first().args[0]).toBe('game-uuid');
	}));

	it('loading a game stores the log in an array', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.log[0]).toEqual(testLog[0]);
		expect(service.log[1]).toEqual(testLog[1]);
		expect(service.log[2]).toEqual(testLog[2]);
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

	it('updateCompany() keeps old company value', fakeAsync(() => {
		let company = Company.fromJson({
			uuid: 'company-uuid-1',
			name: 'PMQ',
			cash: 1,
			game: 'game-uuid',
			share_count: 10,
			ipo_shares: 5,
			bank_shares: 9,
			player_owners: [],
			share_set: [],
			text_color: 'black',
			background_color: 'white'
		});
		service.loadGame('game-uuid');
		tick();
		service.companies['company-uuid-1'].value = 72;
		service.updateCompany(company);
		expect(service.companies['company-uuid-1'].value).toBe(72);
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

	it('updateLog() adds log entry to log', fakeAsync(() => {
		let entry = new LogEntry('new-entry-uuid', 'game-uuid',
								 new Date(2017, 7, 15, 0, 0, 0), 'Test');
		service.loadGame('game-uuid');
		tick();
		service.updateLog(entry);
		expect(service.log[service.log.length - 1]).toBe(entry);
	}));

	it('shareInfo() gives info on share holdings of player', fakeAsync(() => {
		testCompanies[0].text_color = 'color1';
		testCompanies[0].background_color = 'color2';
		testCompanies[1].text_color = 'color3';
		testCompanies[1].background_color = 'color4';
		service.loadGame('game-uuid');
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
			fraction: 0.4,
			shares: 2,
			share_count: 5,
			name: 'C&O',
			text_color: 'black',
			background_color: 'white'
		});
		expect(info[2]).toEqual({
			fraction: 0.3,
			shares: 3,
			share_count: 10,
			name: 'PMQ',
			text_color: 'color3',
			background_color: 'color4'
		});
	}));

	it('shareInfo() sorts by company name', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		let info = service.shareInfo(testPlayers[0]);
		expect(info[0]['name']).toEqual('B&O');
		expect(info[1]['name']).toEqual('C&O');
		expect(info[2]['name']).toEqual('PMQ');
	}));

	it('shareInfo() doesnt include 0 share holdings', fakeAsync(() => {
		testPlayerShares[0].shares = 0;
		service.loadGame('game-uuid');
		tick();
		let info = service.shareInfo(testPlayers[0]);
		expect(info.length).toBe(2);
		expect(info[0]['name']).toBe('B&O');
		expect(info[1]['name']).toBe('C&O');
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

	it('netWorth() returns net worth of a player', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		service.companies['company-uuid-0'].value = 50;
		service.companies['company-uuid-1'].value = 90;
		expect(service.netWorth(service.players['player-uuid-0'])['netWorth'])
			.toBe(100 + 2*50 + 3*90);
	}));

	it('netWorth() returns value of shares in each company', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		service.companies['company-uuid-0'].value = 50;
		service.companies['company-uuid-1'].value = 90;
		let netWorth = service.netWorth(service.players['player-uuid-0']);
		expect(netWorth['company-uuid-0']).toBe(2 * 50);
		expect(netWorth['company-uuid-1']).toBe(3 * 90);
		expect(netWorth['company-uuid-3']).toBe(2 * 0);
	}));

	it('adds error when game does not exist', fakeAsync(() => {
		gameService.getGame.and.callFake(() => Promise.reject({
			_body: {detail: 'Not found.'},
			status: 404,
			statusText: 'Not Found',
			type: 2
		}));
		service.loadGame('game-uuid');
		tick();
		expect(service.isLoaded()).toBe(false);
		expect(errorService.addError.calls.first().args[0])
			.toMatch('^Game not found');
	}));

	it('ownsShare() returns true if entity owns share (player)',
	   fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.ownsShare(testPlayers[0], testCompanies[0]))
			.toBe(true);
	   }));

	it('ownsShare() returns false if entity doesnt own share (player)',
	   fakeAsync(() => {
		testPlayerShares[1].shares = 0;
		service.loadGame('game-uuid');
		tick();
		expect(service.ownsShare(testPlayers[2], testCompanies[0]))
			.toBe(false);
		expect(service.ownsShare(testPlayers[0], testCompanies[0]))
			.toBe(false);
	   }));

	it('ownsShare() returns true if entity owns share (company)',
	   fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.ownsShare(testCompanies[0], testCompanies[0]))
			.toBe(true);
	   }));

	it('ownsShare() returns false if entity doesnt own share(company)',
	   fakeAsync(() => {
		testCompanyShares[0].shares = 0;
		service.loadGame('game-uuid');
		tick();
		expect(service.ownsShare(testCompanies[0], testCompanies[1]))
			.toBe(false);
		expect(service.ownsShare(testCompanies[0], testCompanies[0]))
			.toBe(false);
	   }));

	it('ownsShare() returns false if company is undefined',
	   fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		expect(service.ownsShare(testCompanies[0], undefined)).toBe(false);
	}));

	it('undo() uses UndoService.undo()', fakeAsync(() => {
		service.loadGame('game-uuid');
		tick();
		service.undo();
		expect(undoService.undo.calls.first().args[0]).toBe(testGame);
	}));

	it('undo() should update game instance', fakeAsync(() => {
		let newGame = new Game('game-uuid', 0);
		undoService.undo.and.callFake(() => Promise.resolve({game: newGame}));
		service.loadGame('game-uuid');
		tick();
		service.undo();
		tick();
		expect(service.game).toEqual(newGame);
	}));

	it('undo() should update players when affected', fakeAsync(() => {
		let newPlayer = new Player('test-uuid', 'game-uuid', 'Alice', 7);
		undoService.undo
			.and.callFake(() => Promise.resolve({players: [newPlayer]}));
		service.loadGame('game-uuid');
		tick();
		service.undo();
		tick();
		expect(service.players['test-uuid']).toBe(newPlayer);
	}));

	it('undo() should remove the last log item', fakeAsync(() => {
		expect(service.log.length).toBe(3);
		undoService.undo.and.callFake(() => Promise.resolve({}));
		service.loadGame('game-uuid');
		tick();
		service.undo();
		tick();
		expect(service.log.length).toBe(2);
	}));
});
