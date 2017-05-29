import { Component, OnInit } from '@angular/core';

import { ErrorService } from '../error.service';

@Component({
	selector: 'error-display',
	templateUrl: './error-display.component.html',
	styleUrls: ['./error-display.component.css']
})
export class ErrorDisplayComponent implements OnInit {
	constructor(public errors: ErrorService) { }

	ngOnInit() {
	}
}
