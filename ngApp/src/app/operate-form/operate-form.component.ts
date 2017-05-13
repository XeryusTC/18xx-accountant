import { Component, OnInit, Input } from '@angular/core';

import { Company }          from '../models/company';
import { GameStateService } from '../game-state.service';
import { OperateService }   from '../operate.service';

@Component({
	selector: 'operate-form',
	templateUrl: './operate-form.component.html',
	styleUrls: ['./operate-form.component.css']
})
export class OperateFormComponent implements OnInit {
	public revenue: number = 0;
	@Input() company: Company;

	constructor(
		public gameState: GameStateService,
		private operateService: OperateService
	) { }

	ngOnInit() {
	}

	operate(method: string): void {
		this.operateService.operate(this.company, this.revenue, method)
			.then(result => {
				if ('game' in result)
					this.gameState.updateGame(result.game);
				if ('players' in result)
					for (let player of result.players)
						this.gameState.updatePlayer(player);
				if ('companies' in result)
					for (let company of result.companies)
						this.gameState.updateCompany(company);
			});
	}

	full(): void {
		this.operate('full');
	}

	half(): void {
		this.operate('half');
	}

	withhold(): void {
		this.operate('withhold');
	}
}
