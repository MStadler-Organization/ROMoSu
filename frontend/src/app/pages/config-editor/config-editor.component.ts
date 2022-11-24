import {Component, OnInit} from '@angular/core';
import {ConfigEditorService} from "./config-editor.service";
import {ConfigFileData} from "../../shared/models/interfaces";
import {FormControl, FormGroup} from "@angular/forms";
import {CustomDialogComponent} from "../../shared/components/custom-dialog/custom-dialog.component";
import {MatDialog} from "@angular/material/dialog";

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
  selectedActionType: number = -1


  constructor(public configEditorService: ConfigEditorService, public dialog: MatDialog) {
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
  }

  /**
   * If form is submitted
   */
  onSubmit() {
    if (this.selectedActionType === 0) {
      // save
      this.showProgressBar = true
      this.configEditorService.patchConfig(this.editConfigFormGroup.getRawValue()).subscribe((response) => {
        this.handleSaveConfigResponse(response.status)
        this.refreshTable()
      })
    } else if (this.selectedActionType === 1) {
      // discard
      // do nothing, just reset vars
    } else if (this.selectedActionType === 2) {
      // delete
      this.showProgressBar = true
      this.configEditorService.deleteConfig(this.editConfigFormGroup.getRawValue().id).subscribe((response) => {
        this.handleDelConfigResponse(response.status)
        this.refreshTable()
      })
    } else {
      // error
      console.error(`Invalid action type: ${this.selectedActionType}`)
    }

    // reset vars
    this.selectedActionType = -1
    this.selectedConfig = <ConfigFileData>{}
  }

  /**
   * Caleld when an action button is clicked
   * @param actionType The action type as integer 0=save, 1=discard, 2=delete
   */
  onActionBtnClicked(actionType: number) {
    this.selectedActionType = actionType
  }

  /**
   * Called after a config delete REST response from server. Shows a dialog depending on the status code.
   * @param statusCode the status code of the response as integer
   * @private
   */
  private handleDelConfigResponse(statusCode: number) {
    if (statusCode === 200) {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 1, // create success
          message: 'Successfully deleted monitoring config!'
        },
        autoFocus: false // disable default focus on button
      });
    } else {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create success
          message: 'Unable to delete monitoring config!'
        },
        autoFocus: false // disable default focus on button
      });
    }
    this.showProgressBar = false
  }

  /**
   * Called after a config save REST response from server. Shows a dialog depending on the status code.
   * @param statuscode the status code of the response as integer
   * @private
   */
  private handleSaveConfigResponse(statuscode: number) {
    if (statuscode === 201) {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 1, // create success
          message: 'Successfully saved monitoring config!'
        },
        autoFocus: false // disable default focus on button
      });
    } else {
      this.dialog.open(CustomDialogComponent, {
        data: {
          type: 2, // create success
          message: 'Unable to save monitoring config!'
        },
        autoFocus: false // disable default focus on button
      });
    }
    this.showProgressBar = false
  }

  /**
   * Refreshes the table
   * @private
   */
  private refreshTable() {
    this.showProgressBar = true
    this.configEditorService.getAllConfigs().subscribe((configs: ConfigFileData[]) => {
      this.dataSource = configs
      this.showProgressBar = false
    })
  }
}
