import { Component, OnInit } from '@angular/core';

import { Game } from '../models/game';
import { GameService } from '../game.service';

@Component({
  selector: 'start-game-form',
  templateUrl: './start-game-form.component.html',
  styleUrls: ['./start-game-form.component.css']
})
export class StartGameFormComponent implements OnInit {
	model = new Game('', 12000);

	constructor(private gameService: GameService) { }

	ngOnInit() {
	}

	onSubmit() {
		console.log('submit');
		this.gameService.create(this.model)
			.then(game => {
				console.log(game);
			});
	}
}
