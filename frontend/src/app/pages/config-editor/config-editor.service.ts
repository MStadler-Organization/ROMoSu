import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ConfigFileData} from "../../shared/models/interfaces";

@Injectable({
  providedIn: "root"
})
export class ConfigEditorService {

  private readonly baseApiURL: string;

  constructor(private readonly http: HttpClient) {
    this.baseApiURL = "http://127.0.0.1:8000/";
  }

  /**
   * REST call to server to get all configs
   */
  getAllConfigs(): Observable<ConfigFileData[]> {
    return this.http.get<ConfigFileData[]>(this.baseApiURL + "config-file/");
  }


}
