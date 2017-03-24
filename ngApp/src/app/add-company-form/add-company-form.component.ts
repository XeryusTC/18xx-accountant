import { Component, OnInit, Input } from '@angular/core';
import { Router }                   from '@angular/router';

import { Company }        from '../models/company';
import { CompanyService } from '../company.service';

@Component({
	selector: 'add-company-form',
	templateUrl: './add-company-form.component.html',
	styleUrls: ['./add-company-form.component.css']
})
export class AddCompanyFormComponent implements OnInit {
	model = new Company('', '', '', 0, 10);
	@Input() game_id: string;

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
			});
	}
}
