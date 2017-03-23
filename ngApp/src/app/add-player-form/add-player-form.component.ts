import { Component, OnInit, Input } from '@angular/core';
import { Router }                   from '@angular/router';

import { Player }        from '../models/player';
import { PlayerService } from '../player.service';

const DUPLICATE_PLAYER_ERROR =
	'There is already a player with this name in your game';

@Component({
	selector: 'add-player-form',
	templateUrl: './add-player-form.component.html',
	styleUrls: ['./add-player-form.component.css']
})
export class AddPlayerFormComponent implements OnInit {
	model = new Player('', '', '', 0);
	@Input() game_id: string;
	errors: string[];

	constructor(
		private router: Router,
		private playerService: PlayerService
	) { }

	ngOnInit() {
		this.model.game = this.game_id;
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
				if (error.json()['non_field_errors'][0] ==
					'The fields game, name must make a unique set.') {
					this.errors.push(DUPLICATE_PLAYER_ERROR);
				}
			});
	}
}
