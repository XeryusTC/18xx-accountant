import { Component, OnInit, Input } from '@angular/core';

import { Game } from '../models/game';

@Component({
	selector: 'menu',
	templateUrl: './menu.component.html',
	styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
	@Input() game: Game;

	constructor() { }

	ngOnInit() {
	}
}
