import { Injectable }   from '@angular/core';
import { Http, Headers} from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Company } from './models/company';

@Injectable()
export class OperateService {
	private operateUrl = '/api/operate/';
	private headers = new Headers({'Content-Type': 'application/json'});

	constructor(private http: Http) { }

	operate(company: Company, revenue: number, method: string): Promise<any> {
		let op = {company: company.uuid, amount: revenue, method: method};
		return this.http.post(this.operateUrl,
							  JSON.stringify(op),
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
