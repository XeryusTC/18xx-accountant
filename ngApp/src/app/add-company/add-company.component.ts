import { Component, OnInit }      from '@angular/core';
import { Title }                  from '@angular/platform-browser';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
	selector: 'add-company',
	templateUrl: './add-company.component.html',
	styleUrls: ['./add-company.component.css']
})
export class AddCompanyComponent implements OnInit {
	game_id: string;

	private game_sub;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add company');
		this.game_sub = this.route.params.subscribe((params: Params) =>
			this.game_id = params['uuid']);
	}

	ngOnDestroy() {
		this.game_sub.unsubscribe();
	}
}
