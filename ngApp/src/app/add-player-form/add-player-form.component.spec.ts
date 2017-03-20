import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddPlayerFormComponent } from './add-player-form.component';

describe('AddPlayerFormComponent', () => {
  let component: AddPlayerFormComponent;
  let fixture: ComponentFixture<AddPlayerFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddPlayerFormComponent ]
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
