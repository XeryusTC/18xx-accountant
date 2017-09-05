import { Injectable } from '@angular/core';

import { Company } from './models/company';
import { Player }  from './models/player';

@Injectable()
export class SelectedInstanceService {
	public selectedPlayer: string = null;
	public selectedCompany: string = null;

	selectPlayer(player: Player): void {
		if (this.selectedPlayer == player.uuid) {
			this.selectedPlayer = null;
		} else {
			this.selectedPlayer = player.uuid;
		}
		this.selectedCompany = null;
	}

	selectCompany(company: Company): void {
		if (this.selectedCompany == company.uuid) {
			this.selectedCompany = null;
		} else {
			this.selectedCompany = company.uuid;
		}
		this.selectedPlayer = null;
	}
}
