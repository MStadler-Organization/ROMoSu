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
  name: string;
  save_type: string;
  sum_type_id: number;
  frequencies: number[];
  ecore_data: TreeNodeElement[];
}
