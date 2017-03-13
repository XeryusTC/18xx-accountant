import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Game } from './models/game';

@Injectable()
export class GameService {
	private gameUrl = "/en/api/game/";
	private headers = new Headers({'Content-Type': 'application/json'})

	constructor(private http: Http) { }

	getGames(): Promise<Game[]> {
		return this.http.get(this.gameUrl)
			.toPromise()
			.then(response => response.json() as Game[])
			.catch(this.handleError);
	}

	create(game: Game): Promise<Game> {
		return this.http
			.post(this.gameUrl, JSON.stringify(game), {headers: this.headers})
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error);
		return Promise.reject(error.message || error);
	}
}
