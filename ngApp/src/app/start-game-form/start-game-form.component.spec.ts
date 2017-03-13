import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StartGameFormComponent } from './start-game-form.component';

describe('StartGameFormComponent', () => {
  let component: StartGameFormComponent;
  let fixture: ComponentFixture<StartGameFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StartGameFormComponent ]
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
