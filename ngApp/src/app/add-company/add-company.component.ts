import { Component, OnInit }      from '@angular/core';
import { Title }                  from '@angular/platform-browser';
import { ActivatedRoute, Params } from '@angular/router';

import { GameStateService } from '../game-state.service';

@Component({
	selector: 'add-company',
	templateUrl: './add-company.component.html',
	styleUrls: ['./add-company.component.css']
})
export class AddCompanyComponent implements OnInit {
	private uuid_sub;

	constructor(
		public gameState: GameStateService,
		private titleService: Title,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add company');
		this.uuid_sub = this.route.params.subscribe((params: Params) => {
			if (!this.gameState.isLoaded()) {
				this.gameState.loadGame(params.uuid);
			}
		});
	}

	ngOnDestroy() {
		this.uuid_sub.unsubscribe();
	}
}
