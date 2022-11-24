import {Component, OnInit} from '@angular/core';
import {ConfigEditorService} from "./config-editor.service";
import {ConfigFileData} from "../../shared/models/interfaces";
import {FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-config-editor',
  templateUrl: './config-editor.component.html',
  styleUrls: ['./config-editor.component.scss']
})
export class ConfigEditorComponent implements OnInit {

  showProgressBar: boolean = true
  displayedColumns: string[] = ['id', 'name', 'frequencies', 'save-type', 'sum-type'];
  dataSource: ConfigFileData[] = [];
  selectedConfig: ConfigFileData = <ConfigFileData>{}
  editConfigFormGroup: FormGroup = new FormGroup({
    id: new FormControl({value: '', disabled: true}),
    name: new FormControl(''),
    frequencies: new FormControl(''),
    save_type: new FormControl(''),
    sum_type_id: new FormControl(''),
    ecore_data: new FormControl(''),
  })


  constructor(public configEditorService: ConfigEditorService) {
  }

  /**
   * Default lifecycle hook
   */
  ngOnInit(): void {
    this.configEditorService.getAllConfigs().subscribe((configs: ConfigFileData[]) => {
      this.dataSource = configs
      this.showProgressBar = false
    })
  }

  /**
   * Called when a config-row is clicked
   * @param selectedConfig the config which is clicked on
   */
  onRowClick(selectedConfig: ConfigFileData) {
    this.selectedConfig = selectedConfig

    // beautify json for textarea
    let obj = this.selectedConfig.ecore_data
    if (typeof this.selectedConfig.ecore_data === "string") {
      obj = JSON.parse(this.selectedConfig.ecore_data);
    }
    this.selectedConfig.ecore_data = JSON.stringify(obj, null, 4);

    // set values in form
    this.editConfigFormGroup.setValue(this.selectedConfig)
  }

  /**
   * Returns true, if no config is selected
   */
  isNoConfigSelected() {
    return Object.keys(this.selectedConfig).length === 0
    //  TODO: reset this
  }

  /**
   * If form is submitted
   */
  onSubmit() {
    console.log(this.editConfigFormGroup.value);
  }
}
