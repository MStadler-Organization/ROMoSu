import {Injectable} from "@angular/core";
import {HttpClient, HttpResponse} from "@angular/common/http";
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

  /**
   * REST call to server to delete a config
   */
  deleteConfig(pId: number): Observable<HttpResponse<ConfigFileData>> {
    return this.http.delete<ConfigFileData>(this.baseApiURL + `config-file/?id=${pId}`, {observe: 'response'});
  }


  /**
   * REST call to server to patch a config
   */
  patchConfig(configObj: any): Observable<HttpResponse<ConfigFileData>> {
    return this.http.patch<ConfigFileData>(this.baseApiURL + `config-file/?id=${configObj.id}`, configObj, {observe: 'response'});
  }
}
