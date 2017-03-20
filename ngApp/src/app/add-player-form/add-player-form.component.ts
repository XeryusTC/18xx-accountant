import { Component, OnInit, Input } from '@angular/core';
import { Router }                   from '@angular/router';

import { Player }        from '../models/player';
import { PlayerService } from '../player.service';

@Component({
	selector: 'add-player-form',
	templateUrl: './add-player-form.component.html',
	styleUrls: ['./add-player-form.component.css']
})
export class AddPlayerFormComponent implements OnInit {
	model = new Player('', '', '', 0);
	@Input() game_id: string;

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
			});
	}
}
