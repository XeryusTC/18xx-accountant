import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Title }                  from '@angular/platform-browser';

import 'rxjs/add/operator/switchMap';

import { Game }          from '../models/game';
import { Player }        from '../models/player';
import { Company }       from '../models/company';
import { GameService }   from '../game.service';
import { PlayerService } from '../player.service';
import { CompanyService } from '../company.service';

@Component({
	selector: 'app-game-page',
	templateUrl: './game-page.component.html',
	styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {
	uuid: string;
	game: Game;
	players: Player[] = [];
	companies: Company[] = [];
	selectedPlayer: Player;
	selectedCompany: Company;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute,
		private gameService: GameService,
		private playerService: PlayerService,
		private companyService: CompanyService
	) { }

	getPlayers() {
		for (var player_uuid of this.game.players) {
			this.playerService.getPlayer(player_uuid)
			.then(player => {
				this.players.push(player);
			});
		}
	}

	getCompanies(): void {
		for (var company_uuid of this.game.companies) {
			this.companyService.getCompany(company_uuid)
				.then(company => {
					this.companies.push(company);
				});
		}
	}

	selectPlayer(player: Player): void {
		this.selectedPlayer = player;
		this.selectedCompany = null;
	}

	selectCompany(company: Company): void {
		this.selectedCompany = company;
		this.selectedPlayer = null;
	}

	ngOnInit() {
		this.titleService.setTitle('18xx Accountant')
		this.route.params
		.switchMap((params: Params) =>
				   this.gameService.getGame(params['uuid']))
				   .subscribe((game) => {
					   this.game = game;
					   this.getPlayers();
					   this.getCompanies();
				   });
	}
}
