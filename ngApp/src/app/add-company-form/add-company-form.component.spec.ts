import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { HttpModule }                       from '@angular/http';

import { AddCompanyFormComponent } from './add-company-form.component';

describe('AddCompanyFormComponent', () => {
	let component: AddCompanyFormComponent;
	let fixture: ComponentFixture<AddCompanyFormComponent>;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			declarations: [ AddCompanyFormComponent ],
			imports: [FormsModule, HttpModule]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddCompanyFormComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
