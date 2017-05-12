import { Component, OnInit } from '@angular/core';

import { GameStateService }        from '../game-state.service';
import { SelectedInstanceService } from '../selected-instance.service';

@Component({
	selector: 'player-section',
	templateUrl: './player-section.component.html',
	styleUrls: ['./player-section.component.css']
})
export class PlayerSectionComponent implements OnInit {
	constructor(
		public gameState: GameStateService,
		private selected: SelectedInstanceService
	) { }

	ngOnInit() {
	}
}
