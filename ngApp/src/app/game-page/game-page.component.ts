import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import 'rxjs/add/operator/switchMap';

import { Game }          from '../models/game';
import { Player }        from '../models/player';
import { GameService }   from '../game.service';
import { PlayerService } from '../player.service';

@Component({
	selector: 'app-game-page',
	templateUrl: './game-page.component.html',
	styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {
	uuid: string;
	game: Game;
	players: Player[] = [];

	constructor(
		private route: ActivatedRoute,
		private gameService: GameService,
		private playerService: PlayerService
	) { }

	getPlayers() {
		for (var player_uuid of this.game.players) {
			this.playerService.getPlayer(player_uuid)
			.then(player => {
				this.players.push(player);
			});
		}
	}

	ngOnInit() {
		this.route.params
		.switchMap((params: Params) =>
				   this.gameService.getGame(params['uuid']))
				   .subscribe((game) => {
					   this.game = game;
					   this.getPlayers();
				   });
	}
}
