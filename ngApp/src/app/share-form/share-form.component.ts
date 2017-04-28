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
	source: Company | Player | string = 'ipo';
	@Input() buyer;

	constructor(
		public gameState: GameStateService,
		private transferShareService: TransferShareService
	) { }

	ngOnInit() {
	}

	onSubmit(e: Event) {
		e.preventDefault();
		let company_share = this.gameState.companies[this.company_share];
		this.transferShareService
			.transferShare(this.buyer, company_share, this.source,
						   company_share.value, this.share_amount)
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
				});
	}
}
