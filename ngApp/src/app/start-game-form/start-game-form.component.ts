import { Component, OnInit } from '@angular/core';
import { Router }            from '@angular/router';

import { Game } from '../models/game';
import { GameService } from '../game.service';

@Component({
  selector: 'start-game-form',
  templateUrl: './start-game-form.component.html',
  styleUrls: ['./start-game-form.component.css']
})
export class StartGameFormComponent implements OnInit {
	model = new Game('', 12000);

	constructor(
		private router: Router,
		private gameService: GameService) { }

	ngOnInit() {
	}

	onSubmit() {
		this.gameService.create(this.model)
			.then(game => {
				console.log(game);
				this.router.navigate(['game/', game.uuid]);
			});
	}
}
