import { Component, OnInit, Input } from '@angular/core';

@Component({
	selector: 'menu',
	templateUrl: './menu.component.html',
	styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
	@Input() game_id: string;

	constructor() { }

	ngOnInit() {
	}
}
