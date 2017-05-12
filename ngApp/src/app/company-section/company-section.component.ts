import { Component, OnInit } from '@angular/core';

import { GameStateService }        from '../game-state.service';
import { SelectedInstanceService } from '../selected-instance.service';

@Component({
	selector: 'company-section',
	templateUrl: './company-section.component.html',
	styleUrls: ['./company-section.component.css']
})
export class CompanySectionComponent implements OnInit {
	constructor(
		private gameState: GameStateService,
		private selected: SelectedInstanceService
	) { }

	ngOnInit() {
	}
}
