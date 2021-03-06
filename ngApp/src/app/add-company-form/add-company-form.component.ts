import { Component, OnInit } from '@angular/core';
import { Router }                   from '@angular/router';

import { COLORS }         from '../colors';
import { Company }        from '../models/company';
import { CompanyService } from '../company.service';
import { ColorsService }  from '../colors.service';
import { GameStateService } from '../game-state.service';

const DUPLICATE_COMPANY_ERROR =
	'There is already a company with this name in your game';

@Component({
	selector: 'add-company-form',
	templateUrl: './add-company-form.component.html',
	styleUrls: ['./add-company-form.component.css']
})
export class AddCompanyFormComponent implements OnInit {
	model = new Company('', '', '', 0, 10);
	colors: string[];
	errors: string[];

	constructor(
		private router: Router,
		private companyService: CompanyService,
		private colorsService: ColorsService,
		private gameState: GameStateService
	) { }

	ngOnInit() {
		this.model.game = this.gameState.game.uuid;
		this.getColors();
	}

	onSubmit() {
		this.companyService.create(this.model)
			.then(company => {
				console.log('Created company', company);
				this.router.navigate(['game/', company.game]);
			})
			.catch(error => {
				this.errors = [];
				let errors = error.json();
				/* istanbul ignore else */
				if ('non_field_errors' in errors) {
					this.errors = this.errors
						.concat(errors['non_field_errors']);
				}
			});
	}

	getColors(): void {
		this.colorsService.getColors().then(colors => this.colors = colors);
	}
}
