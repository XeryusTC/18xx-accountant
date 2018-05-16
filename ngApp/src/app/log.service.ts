import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { LogEntry } from './models/log-entry';
import { base_url } from './yourapi_settings';

@Injectable()
export class LogService {
	private logEntryUrl = base_url + '/logentry';
	private headers = new Headers({
    'Content-Type': 'application/json'
	});

	constructor(private http: Http) { }

	getLog(gameUuid: string): Promise<LogEntry[]> {
		return this.http.get(this.logEntryUrl + '?game=' + gameUuid, {headers: this.headers})
			.toPromise()
			.then(response => {
				let res = [];
				for (let entry of response.json()) {
					res.push(LogEntry.fromJson(entry));
				}
				return res;
			})
	}
}
