import { Injectable } from '@angular/core';

import { Game }           from './models/game';
import { Player }         from './models/player';
import { Company }        from './models/company';
import { Share }          from './models/share';
import { LogEntry }       from './models/log-entry';

import { ErrorService }   from './error.service';
import { GameService }    from './game.service';
import { PlayerService }  from './player.service';
import { CompanyService } from './company.service';
import { ShareService }   from './share.service';
import { LogService }     from './log.service';
import { UndoService }    from './undo.service';

export const DIFFERENT_GAME_ERROR = 'This game is different from the old one';
const GAME_NOT_FOUND_ERROR =
	'Game not found. <a href="/">Return to home page</a>.'

@Injectable()
export class GameStateService {
	game: Game;
	players: {[uuid: string]: Player};
	companies: {[uuid: string]: Company};
	shares: {[uuid: string]: Share};
	log: LogEntry[];

	private gameLoaded: boolean = false;
	private playersLoaded: boolean = false;
	private companiesLoaded: boolean = false;
	private playerSharesLoaded: boolean = false;
	private companySharesLoaded: boolean = false;
	private logLoaded: boolean = false;

	constructor(private gameService: GameService,
			    private playerService: PlayerService,
			    private companyService: CompanyService,
				private shareService: ShareService,
				private errorService: ErrorService,
				private logService: LogService,
				private undoService: UndoService
	) { }

	isLoaded(): boolean {
		return (this.gameLoaded && this.playersLoaded && this.companiesLoaded
				&& this.playerSharesLoaded && this.companySharesLoaded
				&& this.logLoaded);
	}

	loadGame(uuid: string): void {
		this.gameLoaded = false;
		this.playersLoaded = false;
		this.companiesLoaded = false;
		this.playerSharesLoaded = false;
		this.companySharesLoaded = false;
		this.logLoaded = false;

		this.gameService.getGame(uuid)
			.then(game => {
				this.game = game;
				this.gameLoaded = true;
				// Get the players
				this.playerService.getPlayerList(game.uuid).then(players => {
					this.players = {};
					for (let player of players) {
						this.players[player.uuid] = player;
					}
					this.playersLoaded = true;
				});
				// Get the companies
				this.companyService.getCompanyList(game.uuid)
					.then(companies => {
						this.companies = {};
						for (let company of companies) {
							this.companies[company.uuid] = company;
						}
						this.companiesLoaded = true;
					});
				// Get the shares
				this.shares = {}
				this.shareService.getPlayerShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
						this.playerSharesLoaded = true;
					});
				this.shareService.getCompanyShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
						this.companySharesLoaded = true;
					});
				// Get the log
				this.logService.getLog(game.uuid)
					.then(log => {
						this.log = log;
						this.logLoaded = true;
					});
			})
			.catch((error: any) => {
				if (error.status == 404) {
					console.error('Game not found');
					this.errorService.addError(GAME_NOT_FOUND_ERROR);
				}
			});
	}

	updateGame(game: Game): void {
		if (game.uuid != this.game.uuid) {
			throw DIFFERENT_GAME_ERROR
		}
		this.game = game;
	}

	updatePlayer(player: Player): void {
		let newPlayers = Object.assign({}, this.players);
		newPlayers[player.uuid] = player;
		this.players = newPlayers;
	}

	updateCompany(company: Company): void {
		company.value = this.companies[company.uuid].value;
		this.companies = Object.assign({}, this.companies);
		this.companies[company.uuid] = company;
	}

	updateShare(share: Share): void {
		this.shares = Object.assign({}, this.shares);
		this.shares[share.uuid] = share;
	}

	updateLog(entry: LogEntry): void {
		this.log.push(entry);
	}

	shareInfo(owner: Player | Company): Object[] {
		let res = [], company;
		for (let share of owner.share_set) {
			if (this.shares[share].shares == 0) {
				continue;
			}
			company = this.companies[this.shares[share].company];
			res.push({
				fraction: this.shares[share].shares / company.share_count,
				shares: this.shares[share].shares,
				share_count: company.share_count,
				name: company.name,
				text_color: company.text_color,
				background_color: company.background_color
			});
		}
		return res.sort((o1, o2) => {
			/* Names can never be equal, so we only need to test one case */
			if (o1['name'] > o2['name']) {
				return 1;
			} else {
				return -1;
			}
		});
	}

	netWorth(player: Player): {[name: string]: number} {
		let worth = {netWorth: player.cash}
		for (let share_uuid of player.share_set) {
			let share: Share = this.shares[share_uuid];
			let value = share.shares * this.companies[share.company].value;
			worth['netWorth'] += value;
			worth[share.company] = value;
		}
		return worth;
	}

	ownsShare(owner: Player | Company, company: Company): boolean {
		if (company === undefined) {
			return false;
		}
		for (let share of owner.share_set) {
			if (this.shares[share].company == company.uuid &&
			    this.shares[share].shares != 0) {
				return true;
			}
		}
		return false;
	}

	undo(): void {
		this.undoService.undo(this.game)
			.then(result => {
				this.log.pop();  // Remove last log entry
				if ('game' in result) {
					this.updateGame(result.game);
				}
				if ('players' in result) {
					for (let player of result.players) {
						this.updatePlayer(player);
					}
				}
				if ('companies' in result) {
					for (let company of result.companies) {
						this.updateCompany(company);
					}
				}
				if ('shares' in result) {
					for (let share of result.shares) {
						this.updateShare(share);
					}
				}
			});
	}

	redo(): void {
		this.undoService.redo(this.game)
			.then(result => {
				if ('game' in result) {
					this.updateGame(result.game);
				}
				if ('players' in result) {
					for (let player of result.players) {
						this.updatePlayer(player);
					}
				}
				if ('companies' in result) {
					for (let company of result.companies) {
						this.updateCompany(company);
					}
				}
				if ('shares' in result) {
					for (let share of result.shares) {
						this.updateShare(share);
					}
				}
				if ('log' in result) {
					this.updateLog(result.log);
				}
			});
	}
}
