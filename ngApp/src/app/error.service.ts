import { Injectable } from '@angular/core';

@Injectable()
export class ErrorService {
	private errors: string[] = [];

	constructor() { }

	addError(error: string): void {
		this.errors.push(error);
	}

	getErrors(): string[] {
		return this.errors;
	}

	hasErrors(): boolean {
		return this.errors.length > 0;
	}

	clean(): void {
		this.errors = [];
	}
}
