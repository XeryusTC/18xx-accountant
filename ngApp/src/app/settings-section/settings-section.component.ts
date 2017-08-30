import { Component, OnInit } from '@angular/core';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'settings-section',
	templateUrl: './settings-section.component.html',
	styleUrls: ['./settings-section.component.css']
})
export class SettingsSectionComponent implements OnInit {
	constructor(public gameState: GameStateService) { }

	ngOnInit() {
	}
}
