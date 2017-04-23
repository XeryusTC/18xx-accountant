import { Component, OnInit, Input } from '@angular/core';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'share-form',
	templateUrl: './share-form.component.html',
	styleUrls: ['./share-form.component.css']
})
export class ShareFormComponent implements OnInit {
	shares: number = 1;
	source: string = 'ipo';
	@Input() buyer;

	constructor(private gameState: GameStateService) { }

	ngOnInit() {
	}
}
