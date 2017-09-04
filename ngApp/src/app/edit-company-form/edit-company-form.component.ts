import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Company }          from '../models/company';
import { ColorsService }    from '../colors.service';
import { GameStateService } from '../game-state.service';

@Component({
	selector: 'edit-company-form',
	templateUrl: './edit-company-form.component.html',
	styleUrls: ['./edit-company-form.component.css']
})
export class EditCompanyFormComponent implements OnInit {
	public colors: string[][];
	public model: Company;

	private uuid_sub;

	constructor(
		private route: ActivatedRoute,
		private colorsService: ColorsService,
		public gameState: GameStateService
	) { }

	ngOnInit() {
		this.colorsService.getColors().then(colors => this.colors = colors);
		this.uuid_sub = this.route.params.subscribe((params: Params) =>
			this.model = this.gameState.companies[params['uuid']]);
	}

	ngOnDestroy() {
		this.uuid_sub.unsubscribe();
	}
}
