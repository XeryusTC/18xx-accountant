import { Component, OnInit } from '@angular/core';

import { LogEntry }         from '../models/log-entry';
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

	entryColorClass(entry: LogEntry): string {
		if (entry.acting_company === null) {
			return '';
		} else {
			let company = this.gameState.companies[entry.acting_company];
			return 'fg-' + company.text_color +
				' bg-' + company.background_color;
		}
	}
}
