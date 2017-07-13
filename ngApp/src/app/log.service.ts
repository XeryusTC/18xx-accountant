import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { LogEntry } from './models/log-entry';

@Injectable()
export class LogService {
	private logEntryUrl = '/api/logentry/';
	private headers = new Headers({'Content-Type': 'application/json'})

	constructor(private http: Http) { }

	getLog(gameUuid: string): Promise<LogEntry[]> {
		return this.http.get(this.logEntryUrl + '?game=' + gameUuid)
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
