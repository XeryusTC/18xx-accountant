import { Component, OnInit, Input } from '@angular/core';

import { Game } from '../models/game';

@Component({
  selector: 'bank-detail',
  templateUrl: './bank-detail.component.html',
  styleUrls: ['./bank-detail.component.css']
})
export class BankDetailComponent implements OnInit {
	@Input() game: Game;

  constructor() { }

  ngOnInit() {
  }

}
