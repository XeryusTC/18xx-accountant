import { Component, OnInit } from '@angular/core';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'log-section',
	templateUrl: './log-section.component.html',
	styleUrls: ['./log-section.component.css']
})
export class LogSectionComponent implements OnInit {
	constructor(public gameState: GameStateService) { }

	ngOnInit() {
	}
}
