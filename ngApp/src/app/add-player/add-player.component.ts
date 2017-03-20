import { Component, OnInit }      from '@angular/core';
import { Title }                  from '@angular/platform-browser';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
	selector: 'app-add-player',
	templateUrl: './add-player.component.html',
	styleUrls: ['./add-player.component.css']
})
export class AddPlayerComponent implements OnInit {
	game_id: string;

	private game_sub;

	constructor(
		private titleService: Title,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add player')
		this.game_sub = this.route.params.subscribe((params: Params) =>
			this.game_id = params['uuid']);
	}

	ngOnDestroy() {
		this.game_sub.unsubscribe();
	}

}
