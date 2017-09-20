import { Injectable }    from '@angular/core';
import { Http, Headers } from '@angular/http';

import { Game } from './models/game';

@Injectable()
export class UndoService {
	private undoUrl = '/api/undo/';
	private redoUrl = '/api/undo/';
	private headers = new Headers({'Content-Type': 'application/json'})
	constructor(private http: Http) { }

	undo(game: Game): Promise<any> {
		let data = {action: 'undo', game: game.uuid};
		return this.http.post(this.undoUrl,
							  JSON.stringify(data),
							  {headers: this.headers})
			.toPromise()
			.then(response => response.json())
			.catch(this.handleError);
	}

	redo(game: Game): Promise<any> {
		let data = {action: 'redo', game: game.uuid};
		return this.http.post(this.redoUrl,
							  JSON.stringify(data),
							  {headers: this.headers})
			.toPromise()
			.then(response => response.json())
			.catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('A HTTP error occured while undoing', error);
		return Promise.reject(error);
	}
}
