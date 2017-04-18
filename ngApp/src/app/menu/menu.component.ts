import { Component, OnInit, Input } from '@angular/core';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'menu',
	templateUrl: './menu.component.html',
	styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
	constructor(private gameState: GameStateService) { }

	ngOnInit() {
	}
}
