import { Component, OnInit } from '@angular/core';

import { GameStateService } from '../game-state.service';
import { NetWorthService }  from '../net-worth.service';

@Component({
	selector: 'net-worth',
	templateUrl: './net-worth.component.html',
	styleUrls: ['./net-worth.component.css']
})
export class NetWorthComponent implements OnInit {
	constructor(
		public gameState: GameStateService,
		public netWorthService: NetWorthService
	) { }

	ngOnInit() {
	}
}
