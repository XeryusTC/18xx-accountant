import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareFormComponent } from './share-form.component';

describe('ShareFormComponent', () => {
	let component: ShareFormComponent;
	let fixture: ComponentFixture<ShareFormComponent>;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ ShareFormComponent ]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(ShareFormComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});

	it('source is ipo by default', () => {
		expect(component.source).toBe('ipo');
	});

	it('amount is one by default', () => {
		expect(component.shares).toBe(1);
	});
});
