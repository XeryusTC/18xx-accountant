import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Company } from './models/company';
import { base_url, token } from './yourapi_settings';

@Injectable()
export class CompanyService {
	private companyUrl = base_url + '/company';
	private headers = new Headers({
    'Authorization': token,
    'Content-Type': 'application/json'
	});

	constructor(private http: Http) { }

	getCompany(uuid: string): Promise<Company> {
		return this.http.get(this.companyUrl + '/' + uuid, {headers: this.headers})
			.toPromise()
			.then(response => Company.fromJson(response.json()))
			.catch(this.handleError);
	}

	getCompanyList(game_uuid: string): Promise<Company[]> {
		return this.http.get(this.companyUrl + '?game=' + game_uuid, {headers: this.headers})
			.toPromise()
			.then(response => {
				let res = [];
				for (let company of response.json()) {
					res.push(Company.fromJson(company));
				}
				return res;
			});
	}

	create(company: Company): Promise<Company> {
		return this.http
			.post(this.companyUrl, JSON.stringify(company),
				  {headers: this.headers})
			.toPromise().then(response => Company.fromJson(response.json()))
			.catch(this.handleError);
	}

	update(company: Company): Promise<Company> {
		return this.http
			.put(this.companyUrl + company.uuid, JSON.stringify(company),
				 {headers: this.headers})
			.toPromise().then(response => Company.fromJson(response.json()))
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error.message, error);
		return Promise.reject(error);
	}
}
