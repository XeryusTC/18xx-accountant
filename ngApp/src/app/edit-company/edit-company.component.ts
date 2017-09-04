import { Component, OnInit } from '@angular/core';
import { Title }             from '@angular/platform-browser';

@Component({
	selector: 'edit-company',
	templateUrl: './edit-company.component.html',
	styleUrls: ['./edit-company.component.css']
})
export class EditCompanyComponent implements OnInit {

	constructor(
		private titleService: Title,
	) { }

	ngOnInit() {
		this.titleService.setTitle('Edit company');
	}

}
