export class LogEntry {
	constructor(
		public uuid: string,
		public game: string,
		public time: string,
		public text: string,
	) { }

	static fromJson(obj) {
		let entry = new LogEntry(obj.uuid, obj.game, obj.time, obj.text);
		return entry;
	}
}
