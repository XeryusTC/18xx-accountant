import { Component, OnInit } from '@angular/core';

import { Game }        from '../models/game';
import { GameService } from '../game.service';

@Component({
	selector: 'app-game-list',
	providers: [GameService],
	templateUrl: './game-list.component.html',
	styleUrls: ['./game-list.component.css']
})
export class GameListComponent implements OnInit {
	games: Game[];

	constructor(private gameService: GameService) { }

	ngOnInit() {
		this.getGames();
	}

	getGames(): void {
		this.gameService.getGames().then(games => this.games = games);
	}
}
