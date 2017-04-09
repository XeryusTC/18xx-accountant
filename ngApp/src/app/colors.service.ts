import { Injectable } from '@angular/core';
import { Http }       from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class ColorsService {
	colorsUrl = '/api/colors/';

	constructor(private http: Http) { }

	getColors(): Promise<any[]> {
		return this.http.get(this.colorsUrl)
			.toPromise()
			.then(response => {
				let data = response.json();
				let rows = [];
				let row = [];
				for (let i=0; i < data.length; i++) {
					if ((i - 2) % 10 == 0) {
						rows.push(row);
						row = [];
					}
					row.push(data[i][0]);
				}
				rows.push(row); // One final push for the last row
				return rows;
			})
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error.message, error);
		return Promise.reject(error);
	}
}
