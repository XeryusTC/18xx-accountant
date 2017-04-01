import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { BaseRequestOptions, Http }         from '@angular/http';
import { MockBackend }                      from '@angular/http/testing';
import { RouterTestingModule }              from '@angular/router/testing';

import { AddCompanyFormComponent } from './add-company-form.component';
import { CompanyService } from '../company.service';

describe('AddCompanyFormComponent', () => {
	let component: AddCompanyFormComponent;
	let fixture: ComponentFixture<AddCompanyFormComponent>;
	let companyServiceStub = {}

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [FormsModule, RouterTestingModule],
			declarations: [ AddCompanyFormComponent ],
			providers: [
				{
					provide: Http, useFactory: (backend, options) => {
						return new Http(backend, options);
					},
					deps: [MockBackend, BaseRequestOptions]
				},
				MockBackend,
				BaseRequestOptions,
				{provide: CompanyService, useValue: companyServiceStub}
			]
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
