/////////// TS INTERFACES ///////////

export interface TreeNodeElement {
  name: string;
  dataType: string;
  isExpandable: boolean;
  isChecked: boolean;
  children?: TreeNodeElement[];
  index: number;
}

export interface Field {
  fieldName: string;
  fieldDataType: string;
}

export interface SumType {
  id: number;
  name: string;
}


export interface ConfigFileData {
  id?: number; // only when already saved
  name: string;
  frequencies: number[];
  save_type: string;
  sum_type_id: number;
  ecore_data: TreeNodeElement[] | string;
}

export interface RTConfig {
  id?: string; // only when already saved
  prefix: string;
  sum_type_id: number;
  config_id: number;
  config_file_data?: ConfigFileData;
  start_time: string;
  selected_topics?: { name: string, last_data: string }[];
  query_time?: string;

}
