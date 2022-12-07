import http from "../http-common";

class LocationDataService {
  getAll() {
    return http.get("/dcim/locations/");
  }

  get(id) {
    console.log(http.get(`/dcim/locations/${id}/`));
    return http.get(`/dcim/locations/${id}/`);
  }

  // create(data) {
  //   return http.post("/dcim/locations/", data);
  // }
  //
  // update(id, data) {
  //   return http.put(`/dcim/locations/${id}/`, data);
  // }
  //
  // delete(id) {
  //   return http.delete(`/dcim/locations/${id}/`);
  // }

}

export default new LocationDataService();
