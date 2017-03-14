import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import 'rxjs/add/operator/switchMap';

import { Game }        from '../models/game';
import { GameService } from '../game.service';

@Component({
	selector: 'app-game-page',
	templateUrl: './game-page.component.html',
	styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {
	uuid: string;
	game: Game;

	constructor(
		private route: ActivatedRoute,
		private gameService: GameService) { }

	ngOnInit() {
		this.route.params
			.switchMap((params: Params) =>
					   this.gameService.getGame(params['uuid']))
			.subscribe(game => this.game = game);
	}
}
