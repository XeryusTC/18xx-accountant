import { Component, OnInit, Input } from '@angular/core';

import { GameStateService } from '../game-state.service';
import { NetWorthService }  from '../net-worth.service';

@Component({
	selector: 'menu',
	templateUrl: './menu.component.html',
	styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
	constructor(
		public gameState: GameStateService,
		public netWorthService: NetWorthService
	) { }

	ngOnInit() {
	}
}
