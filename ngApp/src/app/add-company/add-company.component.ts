import { Component, OnInit }      from '@angular/core';
import { Title }                  from '@angular/platform-browser';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
	selector: 'add-company',
	templateUrl: './add-company.component.html',
	styleUrls: ['./add-company.component.css']
})
export class AddCompanyComponent implements OnInit {
	constructor(
		private titleService: Title,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add company');
	}
}
