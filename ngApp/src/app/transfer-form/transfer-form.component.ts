import { Component, OnInit, Input } from '@angular/core';

import { TransferMoneyService } from '../transfer-money.service';

@Component({
	selector: 'transfer-form',
	templateUrl: './transfer-form.component.html',
	styleUrls: ['./transfer-form.component.css']
})
export class TransferFormComponent {
	amount: number = 0;
	@Input() source;
	target: string = 'bank';

	constructor(private transferMoneyService: TransferMoneyService) { }

	onSubmit(event: Event) {
		event.preventDefault();
		var realTarget;
		if (this.target == 'bank') {
			realTarget = null;
		}

		this.transferMoneyService.transferMoney(this.amount, this.source,
												realTarget)
			.then(result => {
				console.log('Transfer restult', result);
			});
	}
}
