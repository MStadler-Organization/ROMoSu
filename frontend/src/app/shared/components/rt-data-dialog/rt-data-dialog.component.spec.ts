import {ComponentFixture, TestBed} from '@angular/core/testing';

import {RtDataDialogComponent} from './rt-data-dialog.component';

describe('RtDataDialogComponent', () => {
  let component: RtDataDialogComponent;
  let fixture: ComponentFixture<RtDataDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RtDataDialogComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(RtDataDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
