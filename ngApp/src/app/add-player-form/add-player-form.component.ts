import { Component, OnInit } from '@angular/core';
import { Router }                   from '@angular/router';

import { Player }        from '../models/player';
import { PlayerService } from '../player.service';
import { GameStateService } from '../game-state.service';

const DUPLICATE_PLAYER_ERROR =
	'There is already a player with this name in your game';

@Component({
	selector: 'add-player-form',
	templateUrl: './add-player-form.component.html',
	styleUrls: ['./add-player-form.component.css']
})
export class AddPlayerFormComponent implements OnInit {
	model = new Player('', '', '', 0);
	errors: string[];

	constructor(
		private router: Router,
		private playerService: PlayerService,
		private gameState: GameStateService
	) { }

	ngOnInit() {
		this.model.game = this.gameState.game.uuid;
	}

	onSubmit() {
		this.playerService.create(this.model)
			.then(player => {
				console.log(player);
				this.router.navigate(['game/', player.game]);
			})
			.catch(error => {
				this.errors = [];
				console.log(error.json());
				/* istanbul ignore else */
				if ('non_field_errors' in error.json()) {
					this.errors = this.errors
						.concat(error.json()['non_field_errors'])
				}
			});
	}
}
