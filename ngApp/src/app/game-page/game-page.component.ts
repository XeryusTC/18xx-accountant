import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Title }                  from '@angular/platform-browser';

import 'rxjs/add/operator/switchMap';

import { Game }          from '../models/game';
import { Player }        from '../models/player';
import { Company }       from '../models/company';
import { GameStateService } from '../game-state.service';

@Component({
	selector: 'app-game-page',
	templateUrl: './game-page.component.html',
	styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {
	uuid_sub;
	selectedPlayer: Player;
	selectedCompany: Company;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute,
		private gameState: GameStateService
	) { }

	selectPlayer(player: Player): void {
		this.selectedPlayer = player;
		this.selectedCompany = null;
	}

	selectCompany(company: Company): void {
		this.selectedCompany = company;
		this.selectedPlayer = null;
	}

	ngOnInit() {
		this.titleService.setTitle('18xx Accountant');
		this.uuid_sub = this.route.params.subscribe((params: Params) =>
			this.gameState.loadGame(params['uuid']));
	}

	ngOnDestroy() {
		this.uuid_sub.unsubscribe();
	}
}
