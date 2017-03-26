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
			.then(response => response.json())
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error.message, error);
		return Promise.reject(error);
	}
}
