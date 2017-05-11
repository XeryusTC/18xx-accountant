import { Injectable } from '@angular/core';

import { Company } from './models/company';
import { Player }  from './models/player';

@Injectable()
export class SelectedInstanceService {
	public selectedPlayer: string = null;
	public selectedCompany: string = null;

	selectPlayer(player: Player): void {
		this.selectedPlayer = player.uuid;
		this.selectedCompany = null;
	}

	selectCompany(company: Company): void {
		this.selectedCompany = company.uuid;
		this.selectedPlayer = null;
	}
}
