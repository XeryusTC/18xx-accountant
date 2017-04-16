import { Injectable } from '@angular/core';

import { Game }           from './models/game';
import { Player }         from './models/player';
import { Company }        from './models/company';

import { GameService }    from './game.service';
import { PlayerService }  from './player.service';
import { CompanyService } from './company.service';

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
}
