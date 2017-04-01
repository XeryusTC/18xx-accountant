import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { RouterTestingModule }              from '@angular/router/testing';

import { AddPlayerFormComponent } from './add-player-form.component';
import { PlayerService }          from '../player.service';

describe('AddPlayerFormComponent', () => {
	let component: AddPlayerFormComponent;
	let fixture: ComponentFixture<AddPlayerFormComponent>;
	let playerServiceStub = {};

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [FormsModule, RouterTestingModule],
			declarations: [ AddPlayerFormComponent ],
			providers: [
				{provide: PlayerService, useValue: playerServiceStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(AddPlayerFormComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
