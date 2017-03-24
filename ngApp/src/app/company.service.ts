import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Company } from './models/company';

@Injectable()
export class CompanyService {
	private companyUrl = '/api/company/';
	private headers = new Headers({'Content-Type': 'application/json'});

	constructor(private http: Http) { }

	getCompany(uuid: string): Promise<Company> {
		return this.http.get(this.companyUrl + uuid + '/')
			.toPromise()
			.then(response => response.json() as Company)
			.catch(this.handleError);
	}

	create(company: Company): Promise<Company> {
		return this.http
			.post(this.companyUrl, JSON.stringify(company),
				  {headers: this.headers})
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error.message, error);
		return Promise.reject(error);
	}
}
