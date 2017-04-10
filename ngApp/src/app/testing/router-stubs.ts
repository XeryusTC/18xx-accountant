// Convenience export
export { ActivatedRoute } from '@angular/router';

import { Component, Directive, Injectable, Input } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
	selector: 'router-outlet',
	template: ''
})
export class RouterOutletStubComponent { }

@Directive({
	selector: '[routerLink]',
	host: {
		'(click)': 'onClick()'
	}
})
export class RouterLinkStubDirective {
	@Input('routerLink') linkParams: any;
	navigatedTo: any = null;

	onClick() {
		this.navigatedTo = this.linkParams;
	}
}

@Injectable()
export class ActivatedRouteStub {
	// ActivatedRoute.params is Observable
	private subject = new BehaviorSubject(this.testParams);
	params = this.subject.asObservable();

	// Test parameters
	private _testParams: {};
	get testParams() { return this._testParams; }
	set testParams(params: {}) {
		this._testParams = params;
		this.subject.next(params);
	}

	// ActivatedRoute.snapshot.params
	get snapshot() {
		return { params: this.testParams };
	}
}

export class RouterStub {
	navigate(parts: string[]) { return parts.join(''); }
	navigateByUrl(url: string) { return url; }
}
