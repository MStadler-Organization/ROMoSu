import {Component, OnInit} from '@angular/core';
import {ConfigEditorService} from "./config-editor.service";
import {ConfigFileData} from "../../shared/models/interfaces";

@Component({
  selector: 'app-config-editor',
  templateUrl: './config-editor.component.html',
  styleUrls: ['./config-editor.component.scss']
})
export class ConfigEditorComponent implements OnInit {

  showProgressBar: boolean = true
  displayedColumns: string[] = ['id', 'name', 'frequencies', 'save-type', 'sum-type'];
  dataSource: ConfigFileData[] = [];


  constructor(public configEditorService: ConfigEditorService) {
  }

  ngOnInit(): void {
    this.configEditorService.getAllConfigs().subscribe((configs: ConfigFileData[]) => {
      this.dataSource = configs
      this.showProgressBar = false
    })
  }

  onRowClick(row: any) {
    console.log(row)
  }
}
