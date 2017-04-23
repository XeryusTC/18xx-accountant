import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule }             from '@angular/core';
import { FormsModule }          from '@angular/forms';
import { HttpModule }           from '@angular/http';

import { GameService }          from './game.service';
import { GameStateService }     from './game-state.service';
import { PlayerService }        from './player.service';
import { CompanyService }       from './company.service';
import { TransferMoneyService } from './transfer-money.service';

import { ValuesPipe } from './values.pipe';

import { AddCompanyComponent }     from './add-company/add-company.component';
import { AddCompanyFormComponent } from
	'./add-company-form/add-company-form.component';
import { AddPlayerComponent }      from './add-player/add-player.component';
import { AddPlayerFormComponent }  from
	'./add-player-form/add-player-form.component';
import { AppComponent }            from './app.component';
import { BankDetailComponent }     from './bank-detail/bank-detail.component';
import { GameRoutingModule }       from './game-routing.module';
import { GamePageComponent }       from './game-page/game-page.component';
import { MenuComponent }           from './menu/menu.component';
import { StartPageComponent }      from './start-page/start-page.component';
import { StartGameFormComponent }  from
	'./start-game-form/start-game-form.component';
import { TransferFormComponent }   from
	'./transfer-form/transfer-form.component';
import { ShareFormComponent } from './share-form/share-form.component';

@NgModule({
	declarations: [
		AppComponent,
		StartGameFormComponent,
		StartPageComponent,
		GamePageComponent,
		BankDetailComponent,
		MenuComponent,
		AddPlayerComponent,
		AddPlayerFormComponent,
		AddCompanyComponent,
		AddCompanyFormComponent,
		ValuesPipe,
		TransferFormComponent,
		ShareFormComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule,
		GameRoutingModule
	],
	providers: [
		GameStateService,
		GameService,
		PlayerService,
		CompanyService,
		TransferMoneyService,
		Title
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
