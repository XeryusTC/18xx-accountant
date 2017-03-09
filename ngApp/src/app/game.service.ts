import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Game } from './game';
import { GAMES } from './mock-games';

@Injectable()
export class GameService {
	private gameUrl = "/en/api/game/";

	constructor(private http: Http) { }

	getGames(): Promise<Game[]> {
		return this.http.get(this.gameUrl)
			.toPromise()
			.then(response => response.json() as Game[])
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error);
		return Promise.reject(error.message || error);
	}
}
