import { Component, OnInit, Input } from '@angular/core';
import { Router }                   from '@angular/router';

import { COLORS }         from '../colors';
import { Company }        from '../models/company';
import { CompanyService } from '../company.service';
import { ColorsService }  from '../colors.service';

const DUPLICATE_COMPANY_ERROR =
	'There is already a company with this name in your game';

@Component({
	selector: 'add-company-form',
	providers: [ ColorsService ],
	templateUrl: './add-company-form.component.html',
	styleUrls: ['./add-company-form.component.css']
})
export class AddCompanyFormComponent implements OnInit {
	model = new Company('', '', '', 0, 10);
	colors: string[];
	@Input() game_id: string;
	errors: string[];

	constructor(
		private router: Router,
		private companyService: CompanyService,
		private colorsService: ColorsService
	) { }

	ngOnInit() {
		this.model.game = this.game_id;
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
				if ('non_field_errors' in errors) {
					this.errors = this.errors
						.concat(errors['non_field_errors']);
				}
			});
	}

	getColors(): void {
		this.colorsService.getColors().then(colors => this.colors = colors);
	}

	colorRows(): string[] {
		let rows = [];
		let row = [];
		let specials = [];
		for (let i=0; i<= this.colors.length; i++) {
			if ((i - 2) % 10 == 0) {
				rows.push(row);
				row = [];
			}
			row.push(this.colors[i]);
		}
		return rows;
	}
}
