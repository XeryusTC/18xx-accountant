import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Game } from './models/game';
import { base_url } from './yourapi_settings';

@Injectable()
export class GameService {
	private gameUrl = base_url + "/game/";
	private headers = new Headers({
    'Content-Type': 'application/json'
	});

	constructor(private http: Http) { }

	getGames(): Promise<Game[]> {
		return this.http.get(this.gameUrl, {headers: this.headers})
			.toPromise()
			.then(response => {
				let res = [];
				for (let game of response.json()) {
					res.push(Game.fromJson(game));
				}
				return res;
			})
			.catch(this.handleError);
	}

	getGame(uuid: string): Promise<Game> {
		return this.http.get(this.gameUrl + uuid + '/', {headers: this.headers})
			.toPromise()
			.then(response => Game.fromJson(response.json()))
			.catch(this.handleError);
	}

	create(game: Game): Promise<Game> {
		return this.http
			.post(this.gameUrl, JSON.stringify(game), {headers: this.headers})
			.toPromise().then(response => Game.fromJson(response.json()))
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error);
		return Promise.reject(error);
	}
}
