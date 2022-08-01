import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewConfigWizardComponent } from './new-config-wizard.component';

describe('NewConfigWizardComponent', () => {
  let component: NewConfigWizardComponent;
  let fixture: ComponentFixture<NewConfigWizardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewConfigWizardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewConfigWizardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
