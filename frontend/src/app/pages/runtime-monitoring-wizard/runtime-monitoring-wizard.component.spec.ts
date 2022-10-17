import {ComponentFixture, TestBed} from '@angular/core/testing';

import {RuntimeMonitoringWizardComponent} from './runtime-monitoring-wizard.component';

describe('RuntimeMonitoringWizardComponent', () => {
  let component: RuntimeMonitoringWizardComponent;
  let fixture: ComponentFixture<RuntimeMonitoringWizardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RuntimeMonitoringWizardComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(RuntimeMonitoringWizardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
