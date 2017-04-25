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
	private loaded = 4;

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
					this.loaded -= 1;
				});
				// Get the companies
				this.companyService.getCompanyList(game.uuid)
					.then(companies => {
						this.companies = {};
						for (let company of companies) {
							this.companies[company.uuid] = company;
						}
					this.loaded -= 1;
					});
				// Get the shares
				this.shares = {}
				this.shareService.getPlayerShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
						this.loaded -= 1;
					});
				this.shareService.getCompanyShareList(game.uuid)
					.then(shares => {
						for (let share of shares) {
							this.shares[share.uuid] = share;
						}
						this.loaded -= 1;
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

	shareInfo(owner: Player | Company): Object[] {
		let res = [], company;
		console.log('test');
		console.log(owner.share_set);
		for (let share of owner.share_set) {
			console.log(share);
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
		return res;
	}
}
