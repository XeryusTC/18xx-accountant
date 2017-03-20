export class Player {
	shares = [];

	constructor(
		public uuid: string,
		public game: string,
		public name: string,
		public cash: number
	) { }
}
