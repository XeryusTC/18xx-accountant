import { Component, OnInit }              from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';

import { Company }          from '../models/company';
import { ColorsService }    from '../colors.service';
import { CompanyService }   from '../company.service';
import { GameStateService } from '../game-state.service';

@Component({
	selector: 'edit-company-form',
	templateUrl: './edit-company-form.component.html',
	styleUrls: ['./edit-company-form.component.css']
})
export class EditCompanyFormComponent implements OnInit {
	public colors: string[][];
	public model: Company;
	public errors: string[];

	private uuid_sub;

	constructor(
		private route: ActivatedRoute,
		private router: Router,
		private colorsService: ColorsService,
		private companyService: CompanyService,
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

	onSubmit(): void {
		console.log('original model', this.model);
		this.companyService.update(this.model)
			.then(company => {
				console.log('updated company', company);
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
}
