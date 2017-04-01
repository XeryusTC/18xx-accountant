import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule }                      from '@angular/forms';
import { RouterTestingModule }              from '@angular/router/testing';

import { StartGameFormComponent } from './start-game-form.component';
import { GameService }            from '../game.service';

describe('StartGameFormComponent', () => {
	let component: StartGameFormComponent;
	let fixture: ComponentFixture<StartGameFormComponent>;
	let gameServiceStub = {}

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [FormsModule, RouterTestingModule],
			declarations: [ StartGameFormComponent ],
			providers: [
				{provide: GameService, useValue: gameServiceStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(StartGameFormComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
