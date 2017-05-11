import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Title }                  from '@angular/platform-browser';

import 'rxjs/add/operator/switchMap';

import { Game }                    from '../models/game';
import { Player }                  from '../models/player';
import { Company }                 from '../models/company';
import { GameStateService }        from '../game-state.service';
import { SelectedInstanceService } from '../selected-instance.service';

@Component({
	selector: 'app-game-page',
	templateUrl: './game-page.component.html',
	styleUrls: ['./game-page.component.css'],
	providers: [SelectedInstanceService]
})
export class GamePageComponent implements OnInit {
	uuid_sub;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute,
		public gameState: GameStateService,
		public selected: SelectedInstanceService
	) { }

	ngOnInit() {
		this.titleService.setTitle('18xx Accountant');
		this.uuid_sub = this.route.params.subscribe((params: Params) =>
			this.gameState.loadGame(params['uuid']));
	}

	ngOnDestroy() {
		this.uuid_sub.unsubscribe();
	}
}
