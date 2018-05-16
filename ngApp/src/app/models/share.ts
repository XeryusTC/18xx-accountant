export class Share {
	constructor(
		public uuid: string,
		public owner: string,
		public company: string,
		public shares: number
	) { }

	static fromJson(obj): Share {
	  let uuid = obj.uuid || obj._id_;
		let share = new Share(uuid, obj.owner, obj.company, obj.shares);
		return share;
	}
}
