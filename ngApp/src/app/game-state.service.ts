import { Injectable } from '@angular/core';

import { Game }           from './models/game';
import { Player }         from './models/player';
import { Company }        from './models/company';
import { Share }          from './models/share';

import { GameService }    from './game.service';
import { PlayerService }  from './player.service';
import { CompanyService } from './company.service';
import { ShareService }   from './share.service';

export const DIFFERENT_GAME_ERROR = 'This game is different from the old one';

@Injectable()
export class GameStateService {
	game: Game;
	players: {[uuid: string]: Player};
	companies: {[uuid: string]: Company};
	shares: {[uuid: string]: Share};

	constructor(private gameService: GameService,
			    private playerService: PlayerService,
			    private companyService: CompanyService,
				private shareService: ShareService
	) { }

	loadGame(uuid: string): void {
		this.gameService.getGame(uuid)
			.then(game => {
				this.game = game;
				// Get the players
				this.playerService.getPlayerList(game.uuid).then(players => {
					this.players = {};
					for (let player of players) {
						this.players[player.uuid] = player;
					}
				});
				// Get the companies
				this.companyService.getCompanyList(game.uuid)
					.then(companies => {
						this.companies = {};
						for (let company of companies) {
							this.companies[company.uuid] = company;
						}
					});
				// Get the shares
				this.shares = {}
				this.shareService.getPlayerShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
					});
				this.shareService.getCompanyShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
					});
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
		this.companies = Object.assign({}, this.companies);
		this.companies[company.uuid] = company;
	}

	updateShare(share: Share): void {
		this.shares = Object.assign({}, this.shares);
		this.shares[share.uuid] = share;
	}
}
