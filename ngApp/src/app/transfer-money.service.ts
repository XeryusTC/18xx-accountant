import { Injectable }    from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Player }  from './models/player';
import { Company } from './models/company';

@Injectable()
export class TransferMoneyService {
	private transferMoneyUrl = '/api/transfer_money/';
	private headers = new Headers({'Content-Type': 'application/json'})
	constructor(private http: Http) { }

	transferMoney(amount: number, src: Player | Company, dst): Promise<any> {
		//var transfer = {amount: amount, from_player: "", to_player: "",
		//	from_company: "", to_company: ""};
		var transfer = {amount: amount};

		if (src != null) {
			if (src.hasOwnProperty('share_count')) {
				transfer['from_company'] = src.uuid;
			} else if (src != null) {
				transfer['from_player'] = src.uuid;
			}
		}
		if (dst != null) {
			if (dst.hasOwwnProperty('share_count')) {
				transfer['to_company'] = dst.uuid;
			} else if (dst != null) {
				transfer['to_player'] = dst.uuid;
			}
		}

		console.log(transfer, JSON.stringify(transfer));
		return this.http.post(this.transferMoneyUrl, JSON.stringify(transfer),
							  {headers: this.headers})
			.toPromise()
			.then(response => response.json())
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error);
		return Promise.reject(error);
	}
}
