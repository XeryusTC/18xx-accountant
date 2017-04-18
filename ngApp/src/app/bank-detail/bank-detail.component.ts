import { Component, OnInit, Input } from '@angular/core';

import { Game } from '../models/game';
import { GameStateService } from '../game-state.service';

@Component({
	selector: 'bank-detail',
	templateUrl: './bank-detail.component.html',
	styleUrls: ['./bank-detail.component.css']
})
export class BankDetailComponent implements OnInit {
	constructor(private gameState: GameStateService) { }

	ngOnInit() {
	}

}
