import { Injectable }    from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Company } from './models/company';
import { Player }  from './models/player';

@Injectable()
export class TransferShareService {
	private transferShareUrl = '/api/transfer_share/';
	private headers = new Headers({'Content-Type': 'application/json'})

	constructor(private http: Http) { }

	transferShare(buyer: Player | Company | string,
				  company: Company,
				  source: Player | Company | string,
				  price: number,
				  amount: number): Promise<any> {
		let transfer = {price: price, amount: amount, share: company.uuid};

		// Determine where the share comes from
		if (source == 'ipo' || source == 'bank') {
			transfer['source_type'] = source;
		} else if (source.hasOwnProperty('share_count')) {
			transfer['source_type'] = 'company';
			transfer['company_source'] = source['uuid'];
		} else {
			transfer['source_type'] = 'player';
			transfer['player_source'] = source['uuid'];
		}

		// Determine who is buying the share
		if (buyer == 'ipo' || buyer == 'bank') {
			transfer['buyer_type'] = buyer;
		} else if (buyer.hasOwnProperty('share_count')) {
			transfer['buyer_type'] = 'company';
			transfer['company_buyer'] = buyer['uuid'];
		} else {
			transfer['buyer_type'] = 'player';
			transfer['player_buyer'] = buyer['uuid'];
		}


		return this.http.post(this.transferShareUrl,
							  JSON.stringify(transfer),
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
