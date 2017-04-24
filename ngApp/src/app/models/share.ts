export class Share {
	constructor(
		public uuid: string,
		public owner: string,
		public company: string,
		public shares: number
	) { }

	static fromJson(obj): Share {
		let share = new Share(obj.uuid, obj.owner, obj.company, obj.shares);
		return share;
	}
}
