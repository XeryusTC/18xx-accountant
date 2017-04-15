import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Player } from './models/player';

@Injectable()
export class PlayerService {
	private playerUrl = '/api/player/';
	private headers = new Headers({'Content-Type': 'application/json'})

	constructor(private http: Http) { }

	getPlayer(uuid: string): Promise<Player> {
		return this.http.get(this.playerUrl + uuid + '/')
			.toPromise()
			.then(response => Player.fromJson(response.json()))
			.catch(this.handleError);
	}

	create (player: Player): Promise<Player> {
		return this.http
			.post(this.playerUrl, JSON.stringify(player),
				  {headers: this.headers})
			.toPromise().then(response => Player.fromJson(response.json()))
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured', error);
		return Promise.reject(error);
	}
}
