import { Component, OnInit, Input } from '@angular/core';
import { Router }                   from '@angular/router';

import { COLORS }         from '../colors';
import { Company }        from '../models/company';
import { CompanyService } from '../company.service';

const DUPLICATE_COMPANY_ERROR =
	'There is already a company with this name in your game';

@Component({
	selector: 'add-company-form',
	templateUrl: './add-company-form.component.html',
	styleUrls: ['./add-company-form.component.css']
})
export class AddCompanyFormComponent implements OnInit {
	model = new Company('', '', '', 0, 10);
	colors = COLORS;
	@Input() game_id: string;
	errors: string[];

	constructor(
		private router: Router,
		private companyService: CompanyService
	) { }

	ngOnInit() {
		this.model.game = this.game_id;
	}

	onSubmit() {
		this.companyService.create(this.model)
			.then(company => {
				console.log('Created company', company);
				this.router.navigate(['game/', company.game]);
			})
			.catch(error => {
				this.errors = [];
				console.log(error.json());
				if (error.json()['non_field_errors'][0] ==
					'The fields game, name must make a unique set.') {
					this.errors.push(DUPLICATE_COMPANY_ERROR);
				}
			});
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
