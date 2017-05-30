import { Component, OnInit, Input } from '@angular/core';

import { Company }              from '../models/company';
import { Player }               from '../models/player';
import { GameStateService }     from '../game-state.service';
import { TransferShareService } from '../transfer-share.service';

@Component({
	selector: 'share-form',
	templateUrl: './share-form.component.html',
	styleUrls: ['./share-form.component.css']
})
export class ShareFormComponent implements OnInit {
	company_share: string;
	share_amount: number = 1;
	source: string = 'ipo';
	action: string = 'buy';
	@Input() buyer;
	errors: string[];

	constructor(
		public gameState: GameStateService,
		private transferShareService: TransferShareService
	) { }

	ngOnInit() {
	}

	onSubmit(e: Event) {
		e.preventDefault();
		let company_share = this.gameState.companies[this.company_share];
		let realSource;
		let amount = this.share_amount;

		if (this.source in this.gameState.companies) {
			realSource = this.gameState.companies[this.source];
		} else if (this.source in this.gameState.players) {
			realSource = this.gameState.players[this.source];
		} else {
			realSource = this.source;
		}

		if (this.action == 'sell') {
			amount = -this.share_amount;
		}

		this.transferShareService
			.transferShare(this.buyer, company_share, realSource,
						   company_share.value, amount)
				.then(result => {
					if ('game' in result) {
						this.gameState.updateGame(result.game);
					}
					if ('players' in result) {
						for (let player of result.players) {
							this.gameState.updatePlayer(player);
						}
					}
					if ('companies' in result) {
						for (let company of result.companies) {
							this.gameState.updateCompany(company);
						}
					}
					if ('shares' in result) {
						for (let share of result.shares) {
							this.gameState.updateShare(share);
						}
					}
				})
				.catch(error => {
					this.errors = [];
					console.log('Share transfer error', error.json());
					/* istanbul ignore else */
					if ('non_field_errors' in error.json()) {
						this.errors = this.errors
							.concat(error.json()['non_field_errors']);
					}
				});
	}
}
