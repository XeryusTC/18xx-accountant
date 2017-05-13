import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule }             from '@angular/core';
import { FormsModule }          from '@angular/forms';
import { HttpModule }           from '@angular/http';

import { GameService }          from './game.service';
import { GameStateService }     from './game-state.service';
import { PlayerService }        from './player.service';
import { CompanyService }       from './company.service';
import { TransferMoneyService } from './transfer-money.service';
import { TransferShareService } from './transfer-share.service';
import { ShareService }         from './share.service';
import { OperateService }       from './operate.service';

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
import { PlayerSectionComponent } from './player-section/player-section.component';
import { CompanySectionComponent } from './company-section/company-section.component';
import { OperateFormComponent } from './operate-form/operate-form.component';

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
		ShareFormComponent,
		PlayerSectionComponent,
		CompanySectionComponent,
		OperateFormComponent
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
		TransferShareService,
		ShareService,
		OperateService,
		Title
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
