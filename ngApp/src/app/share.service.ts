import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Share } from './models/share';
import { base_url, token } from './yourapi_settings';

@Injectable()
export class ShareService {
	private playerShareUrl = base_url + "/playershare";
	private companyShareUrl = base_url + "/companyshare";
  private headers = new Headers({
    'Authorization': token,
    'Content-Type': 'application/json'
  });

	constructor(private http: Http) { }

	getPlayerShareList(uuid: string, filter: string = 'game'):
		Promise<Share[]> {
		var url = this.playerShareUrl + '?' + filter + '=' + uuid;
		return this.http.get(url, {headers: this.headers}).toPromise()
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
		return this.http.get(url, {headers: this.headers}).toPromise()
			.then(response => {
				let res = [];
				for (let share of response.json())
					res.push(Share.fromJson(share));
				return res
			});
	}
}
