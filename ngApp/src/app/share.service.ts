import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Share } from './models/share';

@Injectable()
export class ShareService {
	private playerShareUrl = "/api/playershare/";
	private companyShareUrl = "/api/companyshare/";

	constructor(private http: Http) { }

	getPlayerShareList(uuid: string, filter: string = 'game'):
		Promise<Share[]> {
		var url = this.playerShareUrl + '?' + filter + '=' + uuid;
		return this.http.get(url).toPromise()
			.then(response => {
				let res = [];
				for (let share of response.json()) {
					res.push(Share.fromJson(share));
				}
				return res
			});
	}

	getCompanyShareList(uuid: string, filter: string = 'game'):
		Promise<Share[]> {
		var url = this.companyShareUrl + '?' + filter + '=' + uuid;
		return this.http.get(url).toPromise()
			.then(response => {
				let res = [];
				for (let share of response.json())
					res.push(Share.fromJson(share));
				return res
			});
	}
}
