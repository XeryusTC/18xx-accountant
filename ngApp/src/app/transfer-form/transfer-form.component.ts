import { Component, OnInit, Input } from '@angular/core';

import { GameStateService }     from '../game-state.service';
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

	constructor(
		private transferMoneyService: TransferMoneyService,
		private gameState: GameStateService
	) { }

	onSubmit(event: Event) {
		event.preventDefault();
		var realTarget;
		/* istanbul ignore else */
		if (this.target == 'bank') {
			realTarget = null;
		} else if (this.gameState.companies.hasOwnProperty(this.target)) {
			realTarget = this.gameState.companies[this.target];
		} else if (this.gameState.players.hasOwnProperty(this.target)) {
			realTarget = this.gameState.players[this.target];
		}

		this.transferMoneyService.transferMoney(this.amount, this.source,
												realTarget)
			.then(result => {
				if ('game' in result) {
					this.gameState.updateGame(result.game);
				}
				if ('players' in result) {
					for (let player of result.players) {
						this.gameState.updatePlayer(player);
					}
				}
				if ('companies' in result)
					for (let company of result.companies)
						this.gameState.updateCompany(company);
			});
	}
}
