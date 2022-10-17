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
  ecore_data: TreeNodeElement[];
}

export interface RTConfig {
  sum_prefix: string;
  sum_type_id: number;
  config_id: number;
}
