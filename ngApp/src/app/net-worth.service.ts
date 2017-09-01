import { Injectable } from '@angular/core';

@Injectable()
export class NetWorthService {
	displayNetWorth: boolean = false;

	constructor() { }

	toggleNetWorthDisplay(): void {
		this.displayNetWorth = !this.displayNetWorth;
	}
}
