import { Injectable } from '@angular/core';

import { Game }           from './models/game';
import { Player }         from './models/player';
import { Company }        from './models/company';

import { GameService }    from './game.service';
import { PlayerService }  from './player.service';
import { CompanyService } from './company.service';

export const DIFFERENT_GAME_ERROR = 'This game is different from the old one';

@Injectable()
export class GameStateService {
	game: Game;
	players: {[uuid: string]: Player};
	companies: {[uuid: string]: Company};

	constructor(private gameService: GameService,
			    private playerService: PlayerService,
			    private companyService: CompanyService) { }

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
}
