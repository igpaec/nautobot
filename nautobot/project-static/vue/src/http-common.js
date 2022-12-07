import axios from "axios";

export default axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-type": "application/json",
    "Authorization": "Token a9fade64c534bb6c3fffee8a07b05f2464d3383e"
  }
});
