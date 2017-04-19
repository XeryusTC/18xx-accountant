import { Component, OnInit }      from '@angular/core';
import { Title }                  from '@angular/platform-browser';

@Component({
	selector: 'app-add-player',
	templateUrl: './add-player.component.html',
	styleUrls: ['./add-player.component.css']
})
export class AddPlayerComponent implements OnInit {
	constructor(
		private titleService: Title
	) { }

	ngOnInit() {
		this.titleService.setTitle('Add player')
	}
}
