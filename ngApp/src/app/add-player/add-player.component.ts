import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Title }                  from '@angular/platform-browser';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'app-add-player',
	templateUrl: './add-player.component.html',
	styleUrls: ['./add-player.component.css']
})
export class AddPlayerComponent implements OnInit {
	private uuid_sub;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute,
		public gameState: GameStateService
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add player');
		this.uuid_sub = this.route.params.subscribe((params: Params) => {
			if (!this.gameState.isLoaded()) {
				this.gameState.loadGame(params.uuid);
			}
		});
	}

	ngOnDestroy() {
		this.uuid_sub.unsubscribe();
	}
}
